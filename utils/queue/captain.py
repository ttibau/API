from utils.response import Response

from random import shuffle


class Captain:
    def __init__(self, players_obj, players, captains, players_list):
        self.players_obj = players_obj
        self.players = players
        self.captains = captains
        self.players_list = players_list

    def given(self):
        """ Assigns the given captins. """

        capt_1_index = self.players["options"]["param"]["capt_1"]
        capt_2_index = self.players["options"]["param"]["capt_2"]

        if self.players["options"]["assigned_teams"]:
            if self.players["list"][
                self.players_list[capt_1_index]] == \
                    self.players["list"][
                        self.players_list[capt_2_index]]:
                return Response(error="Both captains are on the same team")

        self.captains["team_1"] = self.players_list[capt_1_index]
        self.captains["team_2"] = self.players_list[capt_2_index]

    async def elo(self):
        """ Assigns captains based off elo,
                players_elo - value from players.fetch_many.
        """

        player_elo = await self.players_obj.fetch(include_stats=True)
        if player_elo.error:
            return player_elo

        if self.players["options"]["assigned_teams"]:
            for row in player_elo.data:
                if self.players["list"][row["user_id"]] == 1 \
                     and row["user_id"] not in self.captains["team_1"]:
                    self.captains["team_1"] = row["user_id"]
                elif self.players["list"][row["user_id"]] == 2 \
                        and row["user_id"] not in self.captains["team_2"]:
                    self.captains["team_2"] = row["user_id"]
                elif self.players["list"][row["user_id"]] != 1 \
                        and self.players["list"][row["user_id"]] != 2:
                    return Response(error="{} should be None, 1 or 2".format(
                        self.players["list"][row["user_id"]]
                    ))
                else:
                    break
        else:
            self.captains["team_1"] = player_elo.data[0]["user_id"]
            self.captains["team_2"] = player_elo.data[1]["user_id"]

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
