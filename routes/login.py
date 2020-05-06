from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from settings import Config as config

# from utils.responder import responder


class SteamValidate(HTTPEndpoint):
    async def get(self, request):
        """ Validates data given from open ID. """

        validate = await self.obj.login.steam.validate(**request.query_params)

        if validate.error:
            return RedirectResponse("/" + config.login["steam"]["route"])

        # Here we'll need to work out
        # if we require discord oauth
        # or if we should cache the user.


class SteamLogin(HTTPEndpoint):
    async def get(self, request):
        """ Sends them to steam login """

        return RedirectResponse(
            self.obj.login.steam.create
        )
