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
    async def delete(self, request, args):
        """ Deletes match. """

        return responder.render(
            await request.state.league.match(**args).end()
        )

    @use_args({"match_id": fields.String(required=True), })
    async def get(self, request, args):
        """ Gets base details of match. """

        return responder.render(
            await request.state.league.match(**args).get()
        )


class MatchScoreboard(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True), })
    async def get(self, request, args):
        """ Gets scoreboard of match. """

        return responder.render(
            await request.state.league.match(**args).scoreboard()
        )


class MatchClone(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True), })
    async def post(self, request, args):
        """ Clones match. """

        return responder.render(
            await request.state.league.match(**args).clone()
        )
