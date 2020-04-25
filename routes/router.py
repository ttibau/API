from starlette.routing import Route, Mount, WebSocketRoute
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .match import Match

from .errors import Errors

# Routing
class Routes(object):
    def __init__(self, obj):
        # Route object passing.
        league = League
        league.obj = obj

        match = Match
        match.obj = obj

        self.list = [
            Mount("/api", routes=[
                Route("/league", endpoint=league),
                Route("/match", endpoint=match),
            ]),
        ]

        self.exception_handlers = {
            WebargsHTTPException: Errors.arg_expection,
            HTTPException: Errors.http_exception,
        }