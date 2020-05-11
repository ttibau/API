from starlette.responses import JSONResponse, UJSONResponse


class Responder:
    def __init__(self, response):
        self.response = response

    def json(self):
        """ Renders json response
        """

        return JSONResponse(
            {
                "data": self.response.data,
                "error": self.response.error,
            },
            status_code=self.response.status,
            background=self.response.backgroud
        )

    def ujson(self):
        """ Renders json response
        """

        return UJSONResponse(
            {
                "data": self.response.data,
                "error": self.response.error,
            },
            status_code=self.response.status,
            background=self.response.backgroud
        )
