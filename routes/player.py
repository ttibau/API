from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import responder

class Player(HTTPEndpoint):
    pass

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
    async def get(self, request, args):
        """ List info about given players. """
        
        return responder.render(await request.state.league.player().fetch_many(args))