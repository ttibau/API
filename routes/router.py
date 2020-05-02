from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match, MatchClone, MatchScoreboard, \
    MatchSelectPlayer, MatchSelectMap
from .player import Player, PlayerFetch, PlayerValidate
from .list import PlayersList, MatchesList

from .errors import Errors


# Routing
class Routes:
    def __init__(self, obj):
        routes = {
            "league": League,

            "match": Match,
            "match/clone": MatchClone,
            "match/scoreboard": MatchScoreboard,
            "match/select/map": MatchSelectMap,
            "match/select/player": MatchSelectPlayer,

            "player": Player,
            "player/fetch": PlayerFetch,
            "player/validate": PlayerValidate,

            "list/players": PlayersList,
            "list/matches": MatchesList,
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
