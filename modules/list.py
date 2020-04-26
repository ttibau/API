from utils.response import response

class List(object):
    def __init__(self, current_league, limit, offset, search, desc):
        self.current_league = current_league

        self.values = {
            "league_id": self.current_league.league_id,
            "region": self.current_league.region,
            "offset": offset,
            "limit": limit,
            "search": search,
        }

        if desc:
            self.order_by = "DESC"
        else:
            self.order_by = "ASC"

    async def matches(self):
        """ Pulls matches """

        query = """SELECT match_id, timestamp, status, map, server_id,
                          team_1_name, team_2_name, team_1_score, team_2_score,
                          team_1_side, team_2_side
                    FROM scoreboard_total
                    WHERE region = :region AND league_id = :league_id
                        AND (timestamp LIKE :search OR team_1_name LIKE :search OR team_2_name LIKE :search
                                OR map LIKE :search OR match_id = :search)
                        ORDER BY timestamp {}
                        LIMIT :limit, :offset""".format(self.order_by)
        
        return_data = []
        return_data_append = return_data.append
        async for row in self.current_league.obj.database.iterate(query=query, values=self.values):
            return_data_append({
                "match_id": row["match_id"],
                "server_id": row["server_id"],
                "map": row["map"],
                "status": row["status"],
                "timestamp": row["timestamp"],
                "team_1": {
                    "name": row["team_1_name"],
                    "score": row["team_1_score"],
                    "side": row["team_1_side"],
                },
                "team_2": {
                    "name": row["team_2_name"],
                    "score": row["team_2_score"],
                    "side": row["team_2_side"],
                },
            })

        return response(data=return_data)

    async def players(self):
        """ Pulls players """

        query = """SELECT statistics.user_id, IFNULL(statistics.elo, 0) AS elo, IFNULL(statistics.kills, 0) AS kills, 
                          IFNULL(statistics.deaths, 0) AS deaths, IFNULL(statistics.assists, 0) AS assists, IFNULL(statistics.shots, 0) AS shots, IFNULL(statistics.hits, 0) AS hits, IFNULL(statistics.damage, 0) AS damage, 
                          IFNULL(statistics.headshots, 0) AS headshots, IFNULL(statistics.roundswon, 0) AS roundswon, IFNULL(statistics.roundslost, 0) AS roundslost, IFNULL(statistics.wins, 0) AS wins, IFNULL(statistics.ties, 0) AS ties, 
                          IFNULL(statistics.losses, 0) AS losses, users.steam_id, users.discord_id, users.name, users.pfp 
                    FROM statistics
                        INNER JOIN users
                                ON users.user_id = statistics.user_id
                    WHERE statistics.region = :region AND statistics.league_id = :league_id AND (statistics.user_id = :search OR users.steam_id = :search OR users.discord_id = :search
                                                                                                OR users.name LIKE :search)
                    ORDER BY statistics.elo {}
                    LIMIT :limit, :offset""".format(self.order_by)

        return_data = []
        return_data_append = return_data.append
        async for row in self.current_league.obj.database.iterate(query=query, values=self.values):
            return_data_append({
                "name": row["name"],
                "user_id": row["user_id"],
                "steam_id": row["steam_id"],
                "discord_id": row["discord_id"],
                "pfp": row["pfp"],
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
                },
            })

        return response(data=return_data)