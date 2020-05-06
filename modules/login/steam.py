import re
from urllib import parse

from utils.response import response

from settings import Config as config


class Steam:
    open_url = config.steam["endpoint"] + "openid/login/"
    open_id_url = config.steam["endpoint"] + "openid/id/"

    open_id_params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.identity": "http://specs.openid.net\
            /auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net\
            /auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.return_to": config.website + config.login["steam"]["return"],
        "openid.realm": config.website,
    }

    create = open_url + "?" + parse.urlencode(open_id_params)

    def __init__(self, obj):
        self.obj = obj

    async def validate(self, **kwargs):
        """ Validates login data given is correct. """

        if "openid.assoc_handle" in kwargs \
            and "openid.sig" in kwargs \
                and "openid.ns" in kwargs \
                and "openid.signed" in kwargs \
                and "openid.claimed_id" in kwargs:

            kwargs["openid.mode"] = "check_authentication"

            async with self.obj.sessions.aiohttp.get(
                    self.open_url, data=kwargs) as resp:
                if resp == 200:
                    resp_text = await resp.text()

                    if "is_valid:true" in resp_text:
                        steam_id = re.search(
                            r"{}(\d+)".format(self.open_id_url),
                            kwargs["openid.claimed_id"]
                        )

                        if steam_id and steam_id.group(1):
                            return response(
                                data={"steam_id": steam_id.group(1), }
                            )

        return response(error="Failed to validate")
