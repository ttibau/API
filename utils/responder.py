from starlette.responses import JSONResponse

class responder:
    def render(response: object):
        """ Renders API json
                - response, response object.
        """

        return JSONResponse({
            "data": response.data,
            "error": response.error,
        }, status_code=response.status, background=response.backgroud)