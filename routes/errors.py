from starlette.responses import JSONResponse

from utils.response import response
from utils.responder import responder

class Errors(object):
    async def http_exception(request, exc):
        return responder.render(response(error=exc.detail, status=exc.status_code))

    async def arg_expection(request, exc):
        return responder.render(response(error=exc.messages, status=exc.status_code))