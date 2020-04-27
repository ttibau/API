from utils.response import response

from random import shuffle

class Captain(object):
    def __init__(self, obj):
        self.obj = obj

    def given(self, capt_1_index, capt_2_index):
        """ Assigns the given captins. """

        if self.obj.players["options"]["assiged_teams"]:
            if self.obj.players[self.obj.players_list[capt_1_index]] == self.obj.players[self.obj.players_list[capt_2_index]]:
                return response(error="Both captains are on the same team")

        self.obj.captains["team_1"] = self.obj.players_list[capt_1_index]
        self.obj.captains["team_2"] = self.obj.players_list[capt_2_index]

    def elo(self, players_elo):
        """ Assigns captains based off elo,
                players_elo - value from players.fetch_many.
        """

        if self.obj.players["options"]["assiged_teams"]:
            for row in players_elo:
                if self.obj.players[row["user_id"]] == 1 \
                     and not self.obj.captains["team_1"].get(row["user_id"]):
                    self.obj.captains["team_1"] = row["user_id"]
                elif self.obj.players[row["user_id"]] == 2 \
                 and not self.obj.captains["team_2"].get(row["user_id"]):
                    self.obj.captains["team_2"] = row["user_id"]
                elif self.obj.players[row["user_id"]] != (1 or 2):
                    return response(error="{} should be None, 1 or 2".format(self.obj.players[row["user_id"]]))
                else:
                    break
        else:
            self.obj.captains["team_1"] = players_elo[0]["user_id"]
            self.obj.captains["team_2"] = players_elo[1]["user_id"]

    def random(self):
        """ Randomly assigns a captain. """

        shuffle(self.obj.players_list)

        for user_id in self.obj.players_list:
            if not self.obj.players["list"][user_id]:
                if not self.obj.captains["team_1"]:
                    self.obj.captains["team_1"] = user_id
                else:
                    self.obj.captains["team_2"] = user_id
                    break
            else:
                if self.obj.players["list"][user_id] == 1 \
                    and not self.obj.captains["team_1"]:
                    self.obj.captains["team_1"] = user_id
                elif self.obj.players["list"][user_id] == 2 \
                    and not self.obj.captains["team_2"]:
                    self.obj.captains["team_2"] = user_id
                elif self.obj.players["list"][user_id] != (1 or 2):
                    return response(error="{} should be None, 1 or 2".format(self.obj.players["list"][user_id]))
                else:
                    break