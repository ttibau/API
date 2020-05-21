from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match, MatchClone, MatchScoreboard, \
    MatchSelectPlayer, MatchSelectMap
from .player import Player, PlayerFetch, PlayerValidate
from .list import PlayersList, MatchesList
from .user import User

from .errors import Errors


ROUTES = [
    Mount("/api", routes=[
        Route("/league/", League),
        Mount("/match", routes=[
            Route("/", Match),
            Route("/clone/", MatchClone),
            Route("/scoreboard/", MatchScoreboard),
            Mount("/select", routes=[
                Route("/map/", MatchSelectMap),
                Route("/player/", MatchSelectPlayer),
            ]),
        ]),
        Mount("/player", routes=[
            Route("/", Player),
            Route("/fetch/", PlayerFetch),
            Route("/validate/", PlayerValidate),
        ]),
        Mount("/list", routes=[
            Route("/players/", PlayersList),
            Route("/matches/", MatchesList),
        ]),
        Route("/user/", User),
    ])
]

AUTH_BYPASS = []

EXCEPTION_HANDLERS = {
    WebargsHTTPException: Errors.arg_expection,
    HTTPException: Errors.http_exception,
}
