from utils.misc import Misc
from utils.response import response

class QueueCreate(object):
    captains = {"team_1": None, "team_2": None}

    insert = []
    insert_append = insert.append

    data = {
        "details": {},
        "team_1": {},
        "team_2": {},
    }

    def __init__(self, players, maps, team_names, league_id, region, server_id):
        self.match_id = Misc.uuid4()
        self.players = players
        self.maps = maps

        self.players_list = list(self.players["list"].keys())

        self.data["details"]["match_id"] = self.match_id
        self.data["details"]["server_id"] = server_id
        self.data["details"]["league_id"] = league_id
        self.data["details"]["region"] = region

        self.data["details"]["team_1_name"] = Misc.sanitation(team_names["team_1"])
        self.data["details"]["team_2_name"] = Misc.sanitation(team_names["team_2"])

    def assign_player(self, user_id, team, captain):
        """ Assigns player to tell. """

        if team == 1:
            team_dict = self.data["team_1"]
        else:
            team_dict = self.data["team_2"]

        team_dict[user_id] = {
            "captain": captain == 1,
        }

        self.insert_append({
            "match_id": self.match_id,
            "user_id": user_id,
            "captain": captain,
            "team": team,
        })

    def create(self):
        """ Assigns players & captains to given team. """
        
        if self.players["options"]["assiged_teams"]:
            if self.maps["options"]["type"] == ("random" or "given"):
                # Setting match as live
                self.data["details"]["status"] = 1
            else:
                # Setting match as map selection stage
                self.data["details"]["status"] = 2
        else:
            # Setting match as player selection stage
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

            self.assign_player(user_id=user_id, team=team, captain=captain)

    def assign_given(self, capt_1_index, capt_2_index):
        """ Assigns the given captins. """

        if self.players["options"]["assiged_teams"]:
            if self.players[self.players_list[capt_1_index]] == self.players[self.players_list[capt_2_index]]:
                return response(error="Both captains are on the same team")

        self.captains["team_1"] = self.players_list[capt_1_index]
        self.captains["team_2"] = self.players_list[capt_2_index]

    def assign_elo(self, players_elo):
        """ Assigns captains based off elo,
                players_elo - value from players.fetch_many.
        """

        if self.players["options"]["assiged_teams"]:
            for row in players_elo:
                if self.players[row["user_id"]] == 1 \
                     and not self.captains["team_1"].get(row["user_id"]):
                    self.captains["team_1"] = row["user_id"]
                elif self.players[row["user_id"]] == 2 \
                 and not self.captains["team_2"].get(row["user_id"]):
                    self.captains["team_2"] = row["user_id"]
                elif self.players[row["user_id"]] != (1 or 2):
                    return response(error="{} should be None, 1 or 2".format(self.players[row["user_id"]]))
                else:
                    break
        else:
            self.captains["team_1"] = players_elo[0]["user_id"]
            self.captains["team_2"] = players_elo[1]["user_id"]

    def assign_random(self):
        """ Randomly assigns a captain. """

        players_shuffled = Misc.list_random(self.players_list)

        for user_id in players_shuffled:
            if not self.players["list"][user_id]:
                if not self.captains["team_1"]:
                    self.captains["team_1"] = user_id
                else:
                    self.captains["team_2"] = user_id
                    break
            else:
                if self.players["list"][user_id] == 1 \
                    and not self.captains["team_1"]:
                    self.captains["team_1"] = user_id
                elif self.players["list"][user_id] == 2 \
                    and not self.captains["team_2"]:
                    self.captains["team_2"] = user_id
                elif self.players["list"][user_id] != (1 or 2):
                    return response(error="{} should be None, 1 or 2".format(self.players["list"][user_id]))
                else:
                    break