from utils.response import Response

from models.player import PlayerModel


class Players:
    def __init__(self, current_league, user_ids: list):
        self.current_league = current_league

        self.values = {
            "user_ids": user_ids,
        }

    async def fetch(self, include_stats=False):
        """ Selects given players. """

        values = dict(self.values)

        if include_stats:
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
                              users.discord_id, users.name,
                              users.user_id, users.file_type,
                              users.steam_id, users.joined
                    FROM users
                        LEFT JOIN statistics
                                ON users.user_id = statistics.user_id
                                   AND statistics.league_id = :league_id
                                   AND statistics.region = :region
                    WHERE users.user_id IN :user_ids
                    ORDER BY statistics.elo DESC"""

            values["league_id"] = self.current_league.league_id
            values["region"] = self.current_league.region
        else:
            query = """SELECT discord_id, name, user_id, steam_id, joined
                       FROM users WHERE user_id IN :user_ids"""

        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj\
                .database.iterate(query=query, values=values):

            player = PlayerModel(row)

            if include_stats:
                rows_formatted_append(player.full)
            else:
                rows_formatted_append(player.minimal)

        return Response(data=rows_formatted)

    async def validate(self):
        """ Validates given users & returns data of users who aren't valid. """

        user_ids = list(self.values["user_ids"])
        user_ids_remove = user_ids.remove

        query = """SELECT user_id FROM users
                   WHERE user_id IN :user_ids"""

        async for row in self.current_league.obj.database.iterate(
                query=query,
                values=self.values):
            user_ids_remove(row["user_id"])

        if len(user_ids) == 0:
            return Response(data=True)
        else:
            return Response(data=user_ids, error="Invalid user IDs")
