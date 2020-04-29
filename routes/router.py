from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match, MatchList, MatchClone
from .player import Player, PlayerList, PlayerFetch

from .errors import Errors


# Routing
class Routes(object):
    def __init__(self, obj):
        routes = {
            "league": League,

            "match": Match,
            "match/list": MatchList,
            "match/clone": MatchClone,

            "player": Player,
            "player/list": PlayerList,
            "player/fetch_many": PlayerFetch,
        }

        routes_init = []
        for route, route_obj in routes.items():
            route_obj.obj = obj

            routes_init.append(Route("/" + route, endpoint=route_obj))

        self.list = [
            Mount("/api", routes=routes_init),
        ]

        self.exception_handlers = {
            WebargsHTTPException: Errors.arg_expection,
            HTTPException: Errors.http_exception,
        }
