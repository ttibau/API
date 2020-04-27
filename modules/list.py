from utils.response import response

from models.match import MatchModel
from models.player import PlayerModel

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
                          team_1_side, team_2_side,
                          map_order, player_order
                    FROM scoreboard_total
                    WHERE region = :region AND league_id = :league_id
                        AND (timestamp LIKE :search OR team_1_name LIKE :search OR team_2_name LIKE :search
                                OR map LIKE :search OR match_id = :search)
                        ORDER BY timestamp {}
                        LIMIT :limit, :offset""".format(self.order_by)
        
        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj.database.iterate(query=query, values=self.values):
            rows_formatted_append(MatchModel(row).full)

        return response(data=rows_formatted)

    async def players(self):
        """ Pulls players """

        query = """SELECT IFNULL(statistics.elo, 0) AS elo, IFNULL(statistics.kills, 0) AS kills, 
                          IFNULL(statistics.deaths, 0) AS deaths, IFNULL(statistics.assists, 0) AS assists, IFNULL(statistics.shots, 0) AS shots, IFNULL(statistics.hits, 0) AS hits, IFNULL(statistics.damage, 0) AS damage, 
                          IFNULL(statistics.headshots, 0) AS headshots, IFNULL(statistics.roundswon, 0) AS roundswon, IFNULL(statistics.roundslost, 0) AS roundslost, IFNULL(statistics.wins, 0) AS wins, IFNULL(statistics.ties, 0) AS ties, 
                          IFNULL(statistics.losses, 0) AS losses, 
                          users.steam_id, users.discord_id, users.name, users.pfp, users.user_id, users.joined
                    FROM users
                        INNER JOIN statistics
                                ON users.user_id = statistics.user_id
                    WHERE users.region = :region AND users.league_id = :league_id AND (users.user_id = :search OR users.steam_id = :search OR users.discord_id = :search
                                                                                       OR users.name LIKE :search)
                    ORDER BY statistics.elo {}
                    LIMIT :limit, :offset""".format(self.order_by)

        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj.database.iterate(query=query, values=self.values):
            rows_formatted_append(PlayerModel(row).full)

        return response(data=rows_formatted)