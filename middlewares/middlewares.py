from starlette.middleware import Middleware

from .api_key import APIKeyValidation


class Middlewares:
    def __init__(self, obj):
        middlewares = [
            APIKeyValidation,
        ]

        self.list = []

        for middleware_obj in middlewares:
            middleware_obj.obj = obj
            self.list.append(Middleware(middleware_obj))
