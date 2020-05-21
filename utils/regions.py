from sessions import SESSIONS
from settings import Config


class Regions:
    @staticmethod
    async def cache():
        rows = []
        rows_append = rows.append
        async for row in SESSIONS.database.iterate(
                query="SELECT region FROM regions"):
            rows_append(row["region"])

        to_remove = []
        to_remove_append = to_remove.append
        for row in rows:
            if row not in Config.regions.keys():
                to_remove_append(row)

        if len(to_remove) > 0:
            await SESSIONS.database.execute(
                query="DELETE FROM regions WHERE region in (:to_remove)",
                values={"to_remove": to_remove, }
            )

        to_insert = []
        to_insert_append = to_insert.append
        for region in Config.regions.keys():
            if region not in rows:
                to_insert_append({
                    "region": region
                })

        if len(to_insert) > 0:
            await SESSIONS.database.execute_many(
                query="INSERT INTO regions (region) VALUES (:region)",
                values=to_insert
            )
