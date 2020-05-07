from starlette.routing import Route
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match, MatchClone, MatchScoreboard, \
    MatchSelectPlayer, MatchSelectMap
from .player import Player, PlayerFetch, PlayerValidate
from .list import PlayersList, MatchesList

from .errors import Errors


ROUTES = {
    "api": {
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
    },
}

AUTH_BYPASS = []


# Routing
class Routes:
    auth_bypass = []

    list = []

    def __init__(self, obj):
        self.obj = obj

        self._format_bypass()
        self._route_format(ROUTES)

        self.exception_handlers = {
            WebargsHTTPException: Errors.arg_expection,
            HTTPException: Errors.http_exception,
        }

    def _format_bypass(self):
        for bypass in AUTH_BYPASS:
            if bypass[0] != "/":
                forward_slash = "/"
            else:
                forward_slash = ""

            self.auth_bypass.append(forward_slash + bypass)

    def _route_format(self, routes, mount=None):
        for route, route_object in routes.items():
            if type(route_object) == dict:
                self._route_format(route_object, route)
            else:
                self._route_append(route, route_object, mount)

    def _route_append(self, route, route_object, mount):
        route_object.obj = self.obj

        if route[0] != "/":
            forward_slash = "/"
        else:
            forward_slash = ""

        if mount:
            route = "{}{}/{}".format(forward_slash, mount, route)
        else:
            route = forward_slash + route

        self.list.append(Route(route, endpoint=route_object))
