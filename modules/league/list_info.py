from utils.response import Response

from models.match import MatchModel
from models.player import PlayerModel


class List:
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

        query = """SELECT st.match_id, st.timestamp, st.status, st.map, st.server_id,
                          st.team_1_name, st.team_2_name, st.team_1_score,
                          st.team_2_score, st.team_1_side, st.team_2_side,
                          st.map_order, st.player_order, st.record_statistics
                    FROM scoreboard_total AS st
                        LEFT JOIN scoreboard as s
                            ON st.match_id = s.match_id
                    WHERE st.region = :region AND st.league_id = :league_id
                        AND (st.timestamp LIKE :search
                             OR st.team_1_name LIKE :search
                             OR st.team_2_name LIKE :search
                             OR st.map LIKE :search
                             OR st.match_id = :search
                             OR s.user_id = :search)
                        ORDER BY st.timestamp {}
                        LIMIT :limit, :offset""".format(self.order_by)

        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj.database.iterate(
                query=query, values=self.values):
            rows_formatted_append(MatchModel(row).full)

        return Response(data=rows_formatted)

    async def players(self):
        """ Pulls players """

        query = """SELECT IFNULL(statistics.elo, 0) AS elo,
                          IFNULL(statistics.kills, 0) AS kills,
                          IFNULL(statistics.deaths, 0) AS deaths,
                          IFNULL(statistics.assists, 0) AS assists,
                          IFNULL(statistics.shots, 0) AS shots,
                          IFNULL(statistics.hits, 0) AS hits,
                          IFNULL(statistics.damage, 0) AS damage,
                          IFNULL(statistics.headshots, 0) AS headshots,
                          IFNULL(statistics.rounds_won, 0) AS rounds_won,
                          IFNULL(statistics.rounds_lost, 0) AS rounds_lost,
                          IFNULL(statistics.wins, 0) AS wins,
                          IFNULL(statistics.ties, 0) AS ties,
                          IFNULL(statistics.loses, 0) AS loses,
                          users.steam_id, users.discord_id,
                          users.name, users.file_type,
                          users.user_id, users.joined
                    FROM users
                        LEFT JOIN statistics
                                ON users.user_id = statistics.user_id
                                   AND statistics.region = :region
                                   AND statistics.league_id = :league_id
                    WHERE users.user_id = :search OR users.steam_id = :search
                         OR users.discord_id = :search
                         OR users.name LIKE :search
                    ORDER BY statistics.elo {}
                    LIMIT :limit, :offset""".format(self.order_by)

        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj.database.iterate(
                query=query, values=self.values):
            rows_formatted_append(PlayerModel(row).full)

        return Response(data=rows_formatted)
