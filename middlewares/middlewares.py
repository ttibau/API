from starlette.middleware import Middleware

from .api_key import APIKeyValidation


MIDDLEWARES = [
    APIKeyValidation,
]


class Middlewares:
    list = []

    def __init__(self, obj):
        for middleware in MIDDLEWARES:
            middleware.obj = obj
            self.list.append(Middleware(middleware))
