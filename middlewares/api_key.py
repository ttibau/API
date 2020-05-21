from datetime import datetime, timedelta

from settings import Config

from starlette.middleware.base import BaseHTTPMiddleware

from utils.api import Api
from utils.masterkey import MASTER_KEY

from routes.router import AUTH_BYPASS

from memory_cache import IN_MEMORY_CACHE

import modulelift


class APIKeyValidation(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path not in AUTH_BYPASS:
            if "Authorization" not in request.headers or \
                    "league_id" not in request.query_params:
                return Api.unauthorized()

            api_key = request.headers["Authorization"]
            league_id = request.query_params["league_id"]

            if api_key != MASTER_KEY:
                cached_keys = IN_MEMORY_CACHE.api_key_requests

                api_key_request = "{}{}{}{}".format(
                    api_key,
                    league_id,
                    request.url.path,
                    request.method
                )
                if api_key_request in cached_keys:
                    if datetime.now() > cached_keys[api_key_request]:
                        cached_keys.pop(api_key_request, None)
                else:
                    valid = await Api.validate(
                        api_key=api_key,
                        league_id=league_id,
                        request_path=request.url.path,
                        request_method=request.method
                    )

                    if not valid:
                        return Api.unauthorized()
                    else:
                        if len(cached_keys) > Config.cache["max_amount"]:
                            cached_keys = {}

                        cached_keys[api_key_request] = datetime.now() \
                            + timedelta(seconds=Config.cache["max_age"])

            if "region" in request.query_params:
                region = request.query_params["region"].lower()
            else:
                region = None

            request.state.league = modulelift.CLIENT.league(
                league_id=league_id,
                region=region
            )

        return await call_next(request)
