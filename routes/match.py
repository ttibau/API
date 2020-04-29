from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import responder


class Match(HTTPEndpoint):
    @use_args({"players": fields.Dict(required=True),
               "maps": fields.Dict(required=True),
               "team_names": fields.Dict(required=True), },)
    async def post(self, request, args):
        """ Creates match. """

        return responder.render(
            await request.state.league.match().create(**args)
        )

    @use_args({"match_id": fields.String(required=True), })
    async def delete(self, request, match_id):
        """ Deletes match. """

        return responder.render(
            await request.state.league.match(match_id=match_id).end()
        )


class MatchList(HTTPEndpoint):
    @use_args({"limit": fields.Integer(missing=25, min=1, max=50),
               "offset": fields.Integer(missing=25, min=1, max=50),
               "search": fields.String(),
               "desc": fields.Bool(missing=True), })
    async def get(self, request, args):
        """ Gets list of matches. """

        return responder.render(
            await request.state.league.list(**args).matches()
        )
