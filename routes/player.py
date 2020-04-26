from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import responder

class Player(HTTPEndpoint):
    @use_args({"user_id": fields.String(required=True),})
    async def get(self, request, user_id):
        """ Get user. """

        return responder.render(await request.state.league.players(user_id=user_id).get())

    @use_args({"user_id": fields.String(required=True),})
    async def delete(self, request, user_id):
        """ Delete user. """

        return responder.render(await request.state.league.players(user_id=user_id).delete())

    @use_args({"user_id": fields.String(required=True),})
    async def patch(self, request, user_id):
        """ Reset user. """
        
        return responder.render(await request.state.league.players(user_id=user_id).reset())

class PlayerList(HTTPEndpoint):
    @use_args({"limit": fields.Integer(missing=25, min=1, max=50), 
               "offset": fields.Integer(missing=25, min=1, max=50),
               "search": fields.String(),
               "desc": fields.Bool(missing=True),})
    async def get(self, request, args):
        """ List players. """
        
        return responder.render(await request.state.league.list(args).players())

class PlayerFetch(HTTPEndpoint):
    @use_args({"user_ids": fields.List(fields.String(), min=1, max=25, required=True),
               "include_stats": fields.Bool(default=False),})
    async def get(self, request, user_ids, include_stats):
        """ List info about given players. """
        
        return responder.render(
            await request.state.league.players(user_ids=user_ids).fetch_many(include_stats=include_stats)
        )