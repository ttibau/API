class response:
    def __init__(self, data=None, error=False, status=200, backgroud=None):
        """ Response object. """

        # If an error is pased we ensure the correct status code is given.
        if status == 200 and error:
            self.status = 500
        else:
            if data is None and not error:
                error = "No data"
                self.status = 500

            self.status = status

        self.data = data
        self.error = error
        self.backgroud = backgroud
