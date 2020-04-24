from starlette.middleware import Middleware

from .api_key import APIKeyValidation

class Middlewares(object):
    def __init__(self, obj):
        self.api_key_validation = APIKeyValidation
        self.api_key_validation.obj = obj

        self.list = [
            Middleware(self.api_key_validation)
        ]