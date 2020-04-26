from utils.response import response

class Player(object):
    def __init__(self, current_league, user_id):
        self.current_league = current_league

        self.values = {
            "user_id": user_id, 
            "region": current_league.region, 
            "league_id": current_league.league_id
        }

    async def get(self):
        query = """SELECT users.user_id, users.steam_id, users.discord_id, users.name, users.pfp, IFNULL(statistics.total_time, 0) AS total_time, IFNULL(statistics.elo, 0) AS elo, IFNULL(statistics.kills, 0) AS kills, 
                        IFNULL(statistics.deaths, 0) AS deaths, IFNULL(statistics.assists, 0) AS assists, IFNULL(statistics.shots, 0) AS shots, IFNULL(statistics.hits, 0) AS hits, IFNULL(statistics.damage, 0) AS damage, 
                        IFNULL(statistics.headshots, 0) AS headshots, IFNULL(statistics.roundswon, 0) AS roundswon, IFNULL(statistics.roundslost, 0) AS roundslost, IFNULL(statistics.wins, 0) AS wins, IFNULL(statistics.ties, 0) AS ties, 
                        IFNULL(statistics.losses, 0) AS losses
                        FROM users
                        LEFT JOIN statistics
                            ON statistics.user_id = users.user_id
                    WHERE (users.steam_id = :user_id OR users.discord_id = :user_id OR users.user_id = :user_id) AND users.region = :region AND statistics.league_id = :league_id
                """

        row = await self.current_league.obj.database.fetch_one(query=query, values=self.values)
        if row:
            return response(data={
                "name": row["name"],
                "user_id": row["user_id"],
                "steam_id": row["steam_id"],
                "discord_id": row["discord_id"],
                "pfp": row["pfp"],
                "total_time": row["total_time"],
                "ranking": {
                    "elo": row["elo"],
                },
                "statistics": {
                    "kills": row["kills"],
                    "deaths": row["deaths"],
                    "assists": row["assists"],
                    "shots": row["shots"],
                    "hits": row["hits"],
                    "damage": row["damage"],
                    "headshots": row["headshots"],
                    "roundswon": row["roundswon"],
                    "roundslost": row["roundslost"],
                    "wins": row["wins"],
                    "ties": row["ties"],
                    "losses": row["losses"],
                }})
        else:
            return response(error="No data")

    async def reset(self):
        pass

    async def delete(self):
        pass