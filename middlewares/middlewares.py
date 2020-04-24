from starlette.middleware import Middleware

from .api_key import APIKeyValidation

class Middlewares(object):
    def __init__(self, obj):
        api_key_validation = APIKeyValidation
        api_key_validation.obj = obj

        self.list = [
            Middleware(api_key_validation)
        ]