from sessions import SESSIONS
from settings import CONFIG


class Regions:
    @staticmethod
    async def cache():
        rows = []
        rows_append = rows.append
        async for row in SESSIONS.database.iterate(
                query="SELECT region AS region FROM regions"):
            rows_append(row["region"])

        to_insert = []
        to_insert_append = to_insert.append
        for region in list(CONFIG.regions.keys()):
            region_upper = region.upper()
            region_lower = region.lower()

            CONFIG.regions[region_upper] = CONFIG.regions.pop(region)

            if region_lower in CONFIG.server["regions"]:
                CONFIG.server["regions"][
                    region_upper] = CONFIG.server["regions"].pop(region_lower)

            if region_upper not in rows:
                to_insert_append({
                    "region": region_upper
                })

        if len(to_insert) > 0:
            await SESSIONS.database.execute_many(
                query="INSERT INTO regions (region) VALUES (UPPER(:region))",
                values=to_insert
            )
