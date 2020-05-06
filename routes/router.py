from starlette.routing import Route
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match, MatchClone, MatchScoreboard, \
    MatchSelectPlayer, MatchSelectMap
from .player import Player, PlayerFetch, PlayerValidate
from .list import PlayersList, MatchesList
from .login import SteamValidate, SteamLogin

from .errors import Errors

from settings import Config as config


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

    "steam/login": SteamLogin,
    config.login["steam"]["return"]: SteamValidate,
}

AUTH_BYPASS = [
    "steam/login",
    config.login["steam"]["return"],
]


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
            self.auth_bypass.append("/" + bypass)

    def _route_format(self, routes, mount=None):
        for route, route_object in routes.items():
            if type(route_object) == dict:
                self._route_format(route_object, route)
            else:
                self._route_append(route, route_object, mount)

    def _route_append(self, route, route_object, mount):
        route_object.obj = self.obj

        if mount:
            route = "/{}/{}".format(mount, route)
        else:
            route = "/" + route

        self.list.append(Route(route, endpoint=route_object))
