from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import responder

class League(HTTPEndpoint):
    async def get(self, request):
        """ Pulls details of map. """

        return responder.render(await request.state.league.details())

    @use_args({"league_name": fields.Str(min=3, max=32), "league_website": fields.Str(min=3, max=255),
               "websocket_endpoint": fields.Str(min=3, max=255), "discord_prefix": fields.Str(min=1, max=3),
               "sm_message_prefix": fields.Str(min=1, max=24), "knife_round": fields.Bool(),
               "pause": fields.Int(), "surrender": fields.Bool(),
               "warmup_commands_only": fields.Bool(), "captain_choice_time": fields.Bool(),})
    async def post(self, request, args):
        """ Updates league details. """

        return responder.render(await request.state.league.update(args))