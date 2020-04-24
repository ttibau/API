from starlette.responses import JSONResponse

# Annoyingly you can't pass an HTTP object for exceptions here
# So we have to fake the responder.render response.
class Errors(object):
    async def http_exception(request, exc):
        return JSONResponse({"data": None, "error": exc.detail}, status_code=exc.status_code)

    async def arg_expection(request, exc):
        return JSONResponse({"data": None, "error": exc.messages}, status_code=exc.status_code)