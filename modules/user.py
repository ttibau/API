from utils.response import response


class User:
    def __init__(self, obj, user_id):
        self.obj = obj
        self.values = {"user_id": user_id, }

    async def exists(self):
        """ Validates if user exists. """

        query = """SELECT COUNT(*)
                   FROM users
                   WHERE users.user_id = :user_id"""

        count = await self.obj.database.fetch_val(
            query=query,
            values=self.values,
        )

        if count == 1:
            return response(data=True)
        else:
            return response(error=True)
