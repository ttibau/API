from utils.misc import Misc
from utils.response import Response

from sessions import SESSIONS

from .captain import Captain
from .map import Map


class Queue:
    captains = {"team_1": None, "team_2": None}

    users = []
    users_append = users.append

    details = {}

    def __init__(self, players, maps, team_names,
                 server_id, region, league_id, match_id):
        self.players = players

        self.maps = maps

        self.details["match_id"] = match_id
        self.details["server_id"] = server_id

        self.details["league_id"] = league_id
        self.details["region"] = region

        self.details["team_1_name"] = Misc.sanitation(team_names["team_1"])
        self.details["team_2_name"] = Misc.sanitation(team_names["team_2"])

        self.captain = Captain(
            players=self.players,
            captains=self.captains
        )
        self.map = Map(details=self.details, maps=self.maps)

    def assign(self, user_id, team, captain):
        """ Assigns player to tell. """

        self.users_append({
            "match_id": self.details["match_id"],
            "user_id": user_id,
            "captain": captain,
            "team": team,
        })

    async def create(self):
        """ Assigns players & captains to given
            team & also inserts the data into the database.
        """

        if self.maps["options"]["type"] == "random" or \
           self.maps["options"]["type"] == "given":
            map_pool = None

            if self.players["options"]["assiged_teams"]:
                # Setting match as live
                self.details["player_order"] = None
                self.details["status"] = 1
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.players[
                    "options"]["selection"]
                self.details["status"] = 3
        else:
            map_pool = []
            map_pool_append = map_pool.append
            for map_name in self.maps["list"]:
                map_pool_append({
                    "map": map_name,
                    "match_id": self.details["match_id"],
                })

            if self.players["options"]["assiged_teams"]:
                # Setting match as map selection stage
                self.details["player_order"] = None
                self.details["status"] = 2
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.players[
                    "options"]["selection"]
                self.details["status"] = 3

        if self.players["options"]["record_statistics"]:
            self.details["record_statistics"] = 1
        else:
            self.details["record_statistics"] = 0

        team_1_count = 0
        team_2_count = 0

        for user_id, team in self.players["list"].items():
            if self.captains["team_1"] == user_id or \
                    self.captains["team_2"] == user_id:
                captain = 1

                if self.captains["team_1"] == user_id:
                    team = 1
                else:
                    team = 2
            else:
                captain = 0

            if team is None:
                team = 0
            elif team == 1:
                team_1_count += 1
            elif team == 2:
                team_2_count += 1
            else:
                return Response(error="{} isn't a valid team side".format(
                    team
                ))

            self.assign(user_id=user_id, team=team, captain=captain)

        if team_1_count != team_2_count:
            return Response(error="Team 1 & 2 should have a\
                                   even amount of players")

        query = """INSERT INTO scoreboard_total (match_id, league_id,
                                                 status, server_id,
                                                 region, team_1_name,
                                                 team_2_name, map,
                                                 map_order,
                                                 player_order,
                                                 record_statistics)
                                        VALUES  (:match_id, :league_id,
                                                 :status, :server_id,
                                                 :region, :team_1_name,
                                                 :team_2_name, :map,
                                                 :map_order,
                                                 :player_order,
                                                 :record_statistics)"""
        await SESSIONS.database.execute(query=query, values=self.details)

        query = """INSERT INTO scoreboard (match_id, user_id, captain, team)
                   VALUES (:match_id, :user_id, :captain, :team)"""
        await SESSIONS.database.execute_many(query=query, values=self.users)

        if map_pool:
            # If map type is random or given we don't
            # need a map pool.
            query = """INSERT INTO map_pool (match_id, map)
                                     VALUES (:match_id, :map)"""
            await SESSIONS.database.execute_many(query=query, values=map_pool)

        return self.details["match_id"]
