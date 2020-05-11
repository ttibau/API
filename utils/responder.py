from starlette.responses import JSONResponse


class responder:
    @staticmethod
    def render(response):
        """ Renders API json
                - response, response object.
        """

        return JSONResponse({
            "data": response.data,
            "error": response.error,
        }, status_code=response.status, background=response.backgroud)
