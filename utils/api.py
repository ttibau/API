from utils.response import Response
from utils.responder import Responder

from sessions import SESSIONS


class Api:
    @staticmethod
    async def validate(api_key, league_id, request_path, request_method):
        """ Validates the given request depending on the
            api key, league id & the access type
                - api_key, UUID api key.
                - league_id, 2 to 4 letter league ID.
                - request_path, current path trying to be accessed.
                - request_method, method of request (e.g. POST, DELETE etc.)
        """

        query = """SELECT COUNT(*) FROM api_keys
                        INNER JOIN api_permissions
                            ON api_permissions.league_id = api_keys.league_id
                        INNER JOIN api_paths
                            ON api_paths.path_id = api_permissions.path_id
                   WHERE api_keys.key = :api_key
                         AND api_keys.league_id = :league_id
                         AND api_keys.access_level
                             >= api_permissions.access_level
                         AND api_paths.path = :path
                         AND api_keys.active = 1
                         AND api_permissions.method = :method"""

        row = await SESSIONS.database.fetch_val(query=query, values={
            "api_key": api_key,
            "league_id": league_id,
            "path": request_path,
            "method": request_method,
        })

        return row == 1

    @staticmethod
    def unauthorized():
        """ Handles unauthorized requests """

        return Responder(
            Response(error="Unauthorized", status=401)
        ).ujson()
