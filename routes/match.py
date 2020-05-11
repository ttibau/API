from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import Responder


class Match(HTTPEndpoint):
    @use_args({"players": fields.Dict(required=True),
               "maps": fields.Dict(required=True),
               "team_names": fields.Dict(required=True), },)
    async def post(self, request, args):
        """ Creates match. """

        return Responder(
            await request.state.league.match().create(**args)
        ).json()

    @use_args({"match_id": fields.String(required=True), })
    async def delete(self, request, args):
        """ Deletes match. """

        return Responder(
            await request.state.league.match(**args).end()
        ).json()

    @use_args({"match_id": fields.String(required=True), })
    async def get(self, request, args):
        """ Gets base details of match. """

        return Responder(
            await request.state.league.match(**args).get()
        ).json()


class MatchSelectPlayer(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True),
               "user_id": fields.String(required=True), })
    async def post(self, request, args):
        """ Selects player for team. """

        return Responder(
            await request.state.league.match(
                match_id=args["match_id"]
                ).select.player(
                    user_id=args["user_id"]
                    )
        ).ujson()


class MatchSelectMap(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True),
               "map": fields.String(required=True), })
    async def post(self, request, args):
        """ Selects map. """

        return Responder(
            await request.state.league.match(
                match_id=args["match_id"]
                ).select.map(
                    map_id=args["map"]
                    )
        ).ujson()


class MatchScoreboard(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True), })
    async def get(self, request, args):
        """ Gets scoreboard of match. """

        return Responder(
            await request.state.league.match(**args).scoreboard()
        ).json()


class MatchClone(HTTPEndpoint):
    @use_args({"match_id": fields.String(required=True), })
    async def post(self, request, args):
        """ Clones match. """

        return Responder(
            await request.state.league.match(**args).clone()
        ).json()
