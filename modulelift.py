from tables import Tables

from settings import Config as config

from routes.router import Routes
from middlewares.middlewares import Middlewares

from utils.api import Api
from utils.server import Server
from utils.webhook import WebhookSend
from utils.websocket import WebSocket
from utils.cdn import Cdn
from utils.steam import Steam
from utils.proxy import Proxy

from memory_cache import InMemoryCache
from sessions import Sessions

from modules.league import League
from modules.user import User

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

    async def context_init(self):
        """ Should be ran within context of the
            loop.
            Creates all needed sessions & functions what
            require loop context.
        """

        await self.database.connect()

        loop = asyncio.get_event_loop()

        self.sessions.aiohttp = aiohttp.ClientSession(loop=loop)
        self.sessions.proxy = proxy_io(api_key=config.proxyio["key"],
                                       session=self.sessions.aiohttp)
        self.websocket = WebSocket(loop=loop)
        self.webhook = WebhookSend(aiohttp_session=self.sessions.aiohttp)

        self.steam = Steam(obj=self)

        Server(obj=self)
        Cdn(obj=self)

    async def clean_up(self):
        """ Cleans up sessions created in context_init. """

        await self.sessions.aiohttp.close()
        await self.database.disconnect()

    def league(self, league_id, region):

        return League(obj=self, league_id=league_id, region=region)

    def user(self, user_id=None):
        """ Handles interactions with users. """

        return User(obj=self, user_id=user_id)

    def proxy(self, ip):
        return Proxy(obj=self, ip=ip)
