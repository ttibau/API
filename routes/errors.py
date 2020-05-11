from utils.response import response
from utils.responder import responder


class Errors:
    @staticmethod
    async def http_exception(request, exc):
        return responder.render(
            response(error=exc.detail, status=exc.status_code)
        )

    @staticmethod
    async def arg_expection(request, exc):
        return responder.render(
            response(error=exc.messages, status=exc.status_code)
        )
