from utils.response import Response

from random import shuffle


class Captain:
    def __init__(self, players, captains, players_list):
        self.players = players
        self.captains = captains
        self.players_list = players_list

    def given(self):
        """ Assigns the given captins. """

        capt_1_index = self.players["options"]["param"]["capt_1"]
        capt_2_index = self.players["options"]["param"]["capt_2"]

        if self.players["options"]["assiged_teams"]:
            if self.players["list"][
                self.players_list[capt_1_index]] == \
                    self.players["list"][
                        self.players_list[capt_2_index]]:
                return Response(error="Both captains are on the same team")

        self.captains["team_1"] = self.players_list[capt_1_index]
        self.captains["team_2"] = self.players_list[capt_2_index]

    def elo(self, players_elo):
        """ Assigns captains based off elo,
                players_elo - value from players.fetch_many.
        """

        if self.players["options"]["assiged_teams"]:
            for row in players_elo:
                if self.players["list"][row["user_id"]] == 1 \
                     and not self.captains["team_1"].get(row["user_id"]):
                    self.captains["team_1"] = row["user_id"]
                elif self.players["list"][row["user_id"]] == 2 \
                        and not self.captains["team_2"].get(
                            row["user_id"]):
                    self.captains["team_2"] = row["user_id"]
                elif self.players["list"][row["user_id"]] != 1 \
                        and self.players["list"][row["user_id"]] != 2:
                    return Response(error="{} should be None, 1 or 2".format(
                        self.players["list"][row["user_id"]]
                    ))
                else:
                    break
        else:
            self.captains["team_1"] = players_elo[0]["user_id"]
            self.captains["team_2"] = players_elo[1]["user_id"]

    def random(self):
        """ Randomly assigns a captain. """

        shuffle(self.players_list)

        for user_id in self.players_list:
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
                elif self.players["list"][user_id] != 1 \
                        and self.players["list"][user_id] != 2:
                    return Response(error="{} should be None, 1 or 2".format(
                        self.players["list"][user_id]
                    ))
                else:
                    break
