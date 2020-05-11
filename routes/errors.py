from utils.response import Response
from utils.responder import Responder


class Errors:
    @staticmethod
    async def http_exception(request, exc):
        return Responder(
            Response(error=exc.detail, status=exc.status_code)
        ).ujson()

    @staticmethod
    async def arg_expection(request, exc):
        return Responder(
            Response(error=exc.messages, status=exc.status_code)
        ).ujson()
