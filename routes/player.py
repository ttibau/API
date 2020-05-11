from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import Responder


class Player(HTTPEndpoint):
    @use_args({"user_id": fields.String(required=True), })
    async def get(self, request, args):
        """ Get user. """

        return Responder(
            await request.state.league.player(**args).get()
        ).json()

    @use_args({"user_id": fields.String(required=True), })
    async def delete(self, request, args):
        """ Delete user. """

        return Responder(
            await request.state.league.player(**args).delete()
        ).ujson()

    @use_args({"user_id": fields.String(required=True), })
    async def patch(self, request, args):
        """ Reset user. """

        return Responder(
            await request.state.league.player(**args).reset()
        ).ujson()


class PlayerValidate(HTTPEndpoint):
    @use_args({"user_ids": fields.List(
                fields.String(), min=1, max=25, required=True
              ), })
    async def post(self, request, args):
        return Responder(
            await request.state.league.players(**args).validate()
        ).ujson()


class PlayerFetch(HTTPEndpoint):
    @use_args({"user_ids": fields.List(
                fields.String(), min=1, max=25, required=True
              ),
               "include_stats": fields.Bool(default=False), })
    async def get(self, request, args):
        """ List info about given players. """

        return Responder(
            await request.state.league.players(
                user_ids=args["user_ids"]
                ).fetch(
                    include_stats=args["include_stats"]
                    )
        ).ujson()
