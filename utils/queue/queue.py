from utils.misc import Misc
from utils.response import response

from utils.queue.captain import Captain
from utils.queue.map import Map

class Queue:
    captains = {"team_1": None, "team_2": None}

    users = []
    users_append = users.append

    details = {}

    def __init__(self, players, maps, team_names, server_id, obj):
        self.obj = obj
        
        current_league = self.obj.current_league

        self.match_id = Misc.uuid4()

        self.players = players
        self.players_list = list(self.players["list"].keys())

        self.maps = maps
        self.selection_types = current_league.obj.config.pug["selection_types"]

        self.database = current_league.obj.database

        self.details["match_id"] = self.match_id
        self.details["server_id"] = server_id

        self.details["league_id"] = current_league.league_id
        self.details["region"] = current_league.region

        self.current_league = current_league

        self.details["team_1_name"] = Misc.sanitation(team_names["team_1"])
        self.details["team_2_name"] = Misc.sanitation(team_names["team_2"])

        self.captain = Captain(obj=self)
        self.map = Map(obj=self)

    def assign(self, user_id, team, captain):
        """ Assigns player to tell. """

        self.users_append({
            "match_id": self.match_id,
            "user_id": user_id,
            "captain": captain,
            "team": team,
        })

    async def create(self):
        """ Assigns players & captains to given team & also inserts the data into the database. """
        
        if self.maps["options"]["type"] == ("random" or "given"):
            map_pool = None

            if self.players["options"]["assiged_teams"]:
                # Setting match as live
                self.details["player_order"] = None
                self.details["status"] = 1
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.selection_types[self.players["options"]["selection"]]
                self.details["status"] = 3
        else:
            map_pool = []
            map_pool_append = map_pool.append
            for map_name in self.maps:
                map_pool_append({
                    "map": map_name,
                    "match_id": self.match_id,
                })

            if self.players["options"]["assiged_teams"]:
                # Setting match as map selection stage
                self.details["player_order"] = None
                self.details["status"] = 2
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.selection_types[self.players["options"]["selection"]]
                self.details["status"] = 3

        if self.players["options"]["record_statistics"]:
            self.details["record_statistics"] = 1
        else:
            self.details["record_statistics"] = 0

        for user_id, team in self.players["list"].items():
            if team != 1 or team != 2 or team is not None:
                return response(error="{} isn't a valid team side".format(team))

            if team is None:
                team = 0

            if self.captains["team_1"].get(user_id) or \
                self.captains["team_2"].get(user_id):
                captain = 1
            else:
                captain = 0

            self.assign(user_id=user_id, team=team, captain=captain)

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
        await self.database.execute(query=query, values=self.details)

        query = """INSERT INTO scoreboard (match_id, user_id, captain, team) 
                                    VALUES (:match_id, :user_id, :captain, :team)"""
        await self.database.execute_many(query=query, values=self.users)

        if map_pool:
            # If map type is random or given we don't
            # need a map pool.
            query = "INSERT INTO map_pool (match_id, map) VALUES (:match_id, :map)"
            await self.database.execute_many(query=query, values=map_pool)

        self.obj.match_id = self.match_id

        return await self.obj.scoreboard()