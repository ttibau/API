from utils.response import response

from models.player import PlayerModel


class Player:
    def __init__(self, current_league, user_id):
        self.current_league = current_league

        self.values = {
            "user_id": user_id,
            "region": current_league.region,
            "league_id": current_league.league_id,
        }

    async def get(self):
        """ Gets infomation on given player. """

        query = """SELECT users.user_id, users.steam_id,
                          users.discord_id, users.name,
                          users.joined, users.file_type,
                          IFNULL(statistics.total_time, 0) AS total_time,
                          IFNULL(statistics.elo, 0) AS elo,
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
                          IFNULL(statistics.loses, 0) AS loses
                        FROM users
                            LEFT JOIN statistics
                                ON statistics.user_id = users.user_id
                                AND statistics.region = :region
                                AND statistics.league_id = :league_id
                    WHERE users.user_id = :user_id
                """

        row = await self.current_league.obj.database.fetch_one(
            query=query,
            values=self.values
        )

        if row:
            return response(data=PlayerModel(row).full)
        else:
            return response(error="Invalid user")

    async def reset(self):
        """ Resets statistics for given user. """

        query = """UPDATE statistics SET
                   total_time = 0,
                   elo = 0,
                   kills = 0,
                   deaths = 0,
                   assists = 0,
                   shots = 0,
                   hits = 0,
                   damage = 0,
                   headshots = 0,
                   rounds_won = 0,
                   rounds_lost = 0,
                   wins = 0,
                   ties = 0,
                   loses = 0
                   WHERE user_id = :user_id AND region = :region
                         AND league_id = :league_id"""

        await self.current_league.database.execute(
            query=query,
            values=self.values
        )

        return response(data=True)

    async def delete(self):
        """ Deletes statistics for given user. """

        query = """DELETE FROM statistics
                   WHERE user_id = :user_id AND region = :region
                         AND league_id = :league_id"""

        await self.current_league.database.execute(
            query=query,
            values=self.values
        )

        return response(data=True)
