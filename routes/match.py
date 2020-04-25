from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

class Match(HTTPEndpoint):
    @use_args({"players": fields.Dict(required=True), "maps": fields.Dict(required=True),
               "team_names": fields.Dict(required=True),})
    async def post(self, request, args):
        """ Creates match. """

        return self.obj.responder.render(await request.state.league.match.create(args))