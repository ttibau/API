class response:
    def __init__(self, data=None, error=False, status=200, backgroud=None):
        if not data and status == 200:
            error = "No data"

        # If an error is pased we ensure the correct status code is given.
        if status == 200 and error:
            self.status = 500
        else:
            self.status = status

        self.data = data
        self.error = error
        self.backgroud = backgroud