from datetime import datetime, timedelta

from settings import Config as config

from starlette.middleware.base import BaseHTTPMiddleware


class APIKeyValidation(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path not in self.obj.routes.auth_bypass:
            if "Authorization" not in request.headers or \
                    "league_id" not in request.query_params:
                return self.obj.api.unauthorized()

            api_key = request.headers["Authorization"]
            league_id = request.query_params["league_id"]

            if api_key != self.obj.master_key:
                in_memory_cache = self.obj.in_memory_cache.api_key_requests

                api_key_request = "{}{}{}{}".format(
                    api_key,
                    league_id,
                    request.url.path,
                    request.method
                )
                if api_key_request in in_memory_cache:
                    if datetime.now() > in_memory_cache[api_key_request]:
                        in_memory_cache.pop(api_key_request, None)
                else:
                    valid = await self.obj.api.validate(
                        api_key=api_key,
                        league_id=league_id,
                        request_path=request.url.path,
                        request_method=request.method
                    )

                    if not valid:
                        return self.obj.api.unauthorized()
                    else:
                        if len(in_memory_cache) > config.cache["max_amount"]:
                            in_memory_cache = {}

                        in_memory_cache[api_key_request] = datetime.now() \
                            + timedelta(seconds=config.cache["max_age"])

            if "region" in request.query_params:
                region = request.query_params["region"].lower()
            else:
                region = None

            request.state.league = self.obj.league(
                league_id=league_id,
                region=region
            )

        return await call_next(request)
