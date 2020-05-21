from starlette.middleware import Middleware

from .api_key import APIKeyValidation


MIDDLEWARES = [
    Middleware(APIKeyValidation)
]
