from utils.response import response
from utils.responder import responder


class Api(object):
    def __init__(self, obj):
        self.obj = obj

    async def validate(self, api_key, league_id, request_path):
        """ Validates the given request depending on the 
            api key, league id & the access type
                - api_key, UUID api key.
                - league_id, 2 to 4 letter league ID.
                - request_path, current path trying to be accessed.
        """

        query = """SELECT COUNT(*) FROM api_keys
                        INNER JOIN api_permissions
                            ON api_permissions.league_id = api_keys.league_id
                        INNER JOIN api_paths
                            ON api_paths.path_id = api_permissions.path_id
                   WHERE api_keys.key = :api_key
                         AND api_keys.league_id = :league_id
                         AND api_permissions.access_level >= api_keys.access_level 
                         AND api_paths.path = :path"""

        row = await self.obj.database.fetch_val(query=query, values={
            "api_key": api_key,
            "league_id": league_id,
            "path": request_path,
        })

        return row == 1

    def unauthorized(self):
        """ Handles unauthorized requests """

        return responder.render(
            response(error="Unauthorized", status=401)
        )