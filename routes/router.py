from starlette.routing import Route, Mount, WebSocketRoute
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

from .league import League
from .errors import Errors

# Routing
class Routes(object):
    def __init__(self, obj):
        # Route object passing.
        self.league = League
        self.league.obj = obj

        self.list = [
            Mount("/api", routes=[
                Mount("/league", routes=[
                    Route("/", endpoint=self.league),
                ]),
            ]),
        ]

        self.exception_handlers = {
            WebargsHTTPException: Errors.arg_expection,
            HTTPException: Errors.http_exception,
        }