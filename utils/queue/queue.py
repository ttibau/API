from utils.misc import Misc
from utils.response import response

from utils.queue.player import Player
from utils.queue.map import Map

class Queue(object):
    captains = {"team_1": None, "team_2": None}

    users = []
    users_append = users.append

    data = {
        "details": {},
        "team_1": {},
        "team_2": {},
    }

    def __init__(self, players, maps, selection_types, database, team_names, league_id, region, server_id):
        self.match_id = Misc.uuid4()
        self.players = players
        self.maps = maps
        self.selection_types = selection_types

        self.database = database

        self.data["details"]["match_id"] = self.match_id
        self.data["details"]["server_id"] = server_id
        self.data["details"]["league_id"] = league_id
        self.data["details"]["region"] = region

        self.data["details"]["team_1_name"] = Misc.sanitation(team_names["team_1"])
        self.data["details"]["team_2_name"] = Misc.sanitation(team_names["team_2"])

        self.player = Player(obj=self)
        self.map = Map(obj=self)

    def assign(self, user_id, team, captain):
        """ Assigns player to tell. """

        if team == 1:
            team_dict = self.data["team_1"]
        else:
            team_dict = self.data["team_2"]

        team_dict[user_id] = {
            "captain": captain == 1,
            "team": team,
        }

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
                self.data["details"]["player_order"] = None
                self.data["details"]["status"] = 1
            else:
                # Setting match as player selection stage
                self.data["details"]["player_order"] = self.selection_types[self.players["options"]["selection"]]
                self.data["details"]["status"] = 3
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
                self.data["details"]["player_order"] = None
                self.data["details"]["status"] = 2
            else:
                # Setting match as player selection stage
                self.data["details"]["player_order"] = self.selection_types[self.players["options"]["selection"]]
                self.data["details"]["status"] = 3

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
                                                    player_order) 
                                        VALUES  (:match_id, :league_id, 
                                                    :status, :server_id, 
                                                    :region, :team_1_name,
                                                    :team_2_name, :map,
                                                    :map_order,
                                                    :player_order)"""
        await self.database.execute(query=query, values=self.data["details"])

        query = """INSERT INTO scoreboard (match_id, user_id, captain, team) 
                                    VALUES (:match_id, :user_id, :captain, :team)"""
        await self.database.execute_many(query=query, values=self.users)

        if map_pool:
            # If map type is random or given we don't
            # need a map pool.
            query = "INSERT INTO map_pool (match_id, map) VALUES (:match_id, :map)"
            await self.database.execute_many(query=query, values=map_pool)