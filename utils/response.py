class Response:
    def __init__(self, data=None, error=False, status=200, background=None):
        """ Response object. """

        # If an error is passed we ensure the correct status code is given.
        if error and status == 200:
            self.status = 500
        else:
            self.status = status

        self.data = data
        self.error = error
        self.background = background
