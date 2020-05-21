import os

from modules.league import League
from modules.user import User

from sessions import SESSIONS
from aiohttp_session import AIOHTTP


class client:
    def __init__(self):
        """ This client assumes the developer has taken
            the initiative to correctly initialize the needed sessions.
        """

        self.user = User
        self.league = League

    async def startup(self):
        """ Should be ran within context of the
            loop.
            Creates all needed sessions & functions what
            require loop context.
        """

        await SESSIONS.database.connect()

    async def shutdown(self):
        """ Cleans up sessions created in context_init. """

        await AIOHTTP.ClientSession.close()
        await SESSIONS.database.disconnect()


CLIENT = client()
