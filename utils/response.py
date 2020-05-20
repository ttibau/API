class Response:
    def __init__(self, data=None, error=False, status=200, background=None):
        """ Response object. """

        # If an error is passed we ensure the correct status code is given.
        if status == 200 and error:
            self.status = 500
        else:
            if data is None and not error:
                error = "No data"
                self.status = 500

            self.status = status

        self.data = data
        self.error = error
        self.background = background
