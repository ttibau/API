from aiohttp.client_exceptions import ClientError

from starlette.background import BackgroundTask

from datetime import datetime

from urllib.parse import urlparse
from os.path import splitext

from utils.response import Response
from utils.misc import Misc

from models.player import PlayerModel


class User:
    accepted_pfp_types = [
        "gif",
        "jpg",
        "jpeg",
        "png",
    ]

    def __init__(self, obj, user_id):
        self.obj = obj
        self.user_id = user_id

    async def exists(self):
        """ Validates if user exists. """

        query = """SELECT COUNT(*)
                   FROM users
                   WHERE user_id = :user_id"""
        values = {"user_id": self.user_id, }

        count = await self.obj.database.fetch_val(
            query=query,
            values=values,
        )

        return Response(data=bool(count))

    async def external_exists(self, steam_id, discord_id):
        """ Validates if external ID has been used before. """

        query = """SELECT COUNT(*)
                   FROM users
                   WHERE (steam_id = :steam_id
                          AND steam_id IS NOT NULL)
                          OR (discord_id = :discord_id
                               AND discord_id IS NOT NULL)"""
        values = {"steam_id": steam_id, "discord_id": discord_id, }

        count = await self.obj.database.fetch_val(
            query=query,
            values=values,
        )

        if count == 0:
            return Response(data=True)
        else:
            return Response(error="Steam or Discord ID already in use.")

    async def _validate_and_format(self, steam_id,
                                   ip, name,
                                   discord_id, pfp):
        """ Validates given params & formats. """

        exists = await self.external_exists(steam_id, discord_id)
        if exists.error:
            return exists

        steam = await self.obj.steam.get_user(steam_id)
        if steam.error:
            return steam

        if not pfp:
            pfp = steam.data["avatarfull"]

        path = urlparse(pfp).path
        file_type = splitext(path)[1][1:]

        if file_type not in self.accepted_pfp_types:
            return Response(error="File type not supported")

        if ip:
            alt_detection = await self.obj.proxy(ip).alt_detection()

            if alt_detection.error:
                return alt_detection

            if alt_detection.data:
                return Response(error="Alt account")

        if not name:
            name = steam.data["personaname"]

        try:
            async with self.obj.sessions.aiohttp.get(pfp) as resp:
                if resp.status == 200:
                    resp_data = await resp.read()

                    background_task = BackgroundTask(
                        self.obj.cdn.upload,
                        path_key="pfps",
                        data=resp_data,
                        file_name="{}.{}".format(self.user_id, file_type)
                    )
                else:
                    return Response(error="Invalid pfp")
        except ClientError:
            return Response(error="Invalid url")

        return Response(data={
            "steam_id": steam_id,
            "discord_id": discord_id,
            "name": name,
            "file_type": file_type,
            "ip": ip,
        }, background=background_task)

    async def create(self, steam_id,
                     ip=None, name=None,
                     discord_id=None, pfp=None):
        """ Creates user from given steam ID.

            pfp should be a link to a image.

            If name, discord_id or pfp not passed then info from
            steam API will be used instead.

            If IP isn't passed then alt detection isn't done.
        """

        self.user_id = Misc.uuid4()

        validate = await self._validate_and_format(
            steam_id,
            ip,
            name,
            discord_id,
            pfp
        )

        if validate.error:
            return validate

        validate.data["user_id"] = self.user_id

        # Normally sql would handle this,
        # but this saves us from having to do a query
        # for the return.
        validate.data["joined"] = datetime.now()

        query = """INSERT INTO
                   users (
                       user_id,
                       steam_id,
                       discord_id,
                       name,
                       file_type,
                       joined,
                       ip
                   )
                   VALUES (
                       :user_id,
                       :steam_id,
                       :discord_id,
                       :name,
                       :file_type,
                       :joined,
                       :ip
                   )"""

        await self.obj.database.execute(query=query, values=validate.data)

        return Response(
            data=PlayerModel(validate.data).minimal,
            background=validate.background
        )
