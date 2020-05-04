from tables import Tables

from settings import Config as config

from routes.router import Routes
from middlewares.middlewares import Middlewares

from utils.api import Api
from utils.server import Server
from utils.webhook import WebhookSend
from utils.websocket import WebSocket
from utils.cdn import Cdn

from memory_cache import InMemoryCache
from sessions import Sessions

from modules.league import League

import asyncio
import aiohttp
from aioproxyio import proxy_io


class client:
    in_memory_cache = InMemoryCache
    sessions = Sessions

    def __init__(self):
        """ This client assumes the developer has taken
            the initiative to correctly initialize the needed sessions.
        """

        # Creating tables & returning ORM objects back.
        self.tables = Tables(obj=self)

        self.routes = Routes(obj=self)
        self.middlewares = Middlewares(obj=self)
        self.api = Api(obj=self)

    def context_init(self):
        """ Should be ran within context of the
            loop.
            Creates all needed sessions & functions what
            require loop context.
        """

        loop = asyncio.get_event_loop()

        self.sessions.aiohttp = aiohttp.ClientSession(loop=loop)
        self.sessions.proxy = proxy_io(api_key=config.proxyio["key"],
                                       session=self.sessions.aiohttp)
        self.websocket = WebSocket(loop=loop)
        self.webhook = WebhookSend(aiohttp_session=self.sessions.aiohttp)

        Server(obj=self)
        Cdn(obj=self)

    def league(self, league_id, region):

        return League(obj=self, league_id=league_id, region=region)

    async def validate_user(self, user_id):
        """ Returns true or false depending if the
            user exists, context of region or league
            doesn't matter. """

        query = """SELECT COUNT(*)
                FROM users
                WHERE users.user_id = :user_id"""

        values = {"user_id": user_id, }

        count = await self.database.fetch_val(
            query=query,
            values=values,
        )

        return count == 1
