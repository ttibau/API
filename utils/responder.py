from starlette.responses import JSONResponse

class Responder(object):
    def render(self, response):
        """ Renders API json
                - response, response object.
        """

        return JSONResponse({
            "data": response.data,
            "error": response.error,
        }, status_code=response.status, background=response.backgroud)