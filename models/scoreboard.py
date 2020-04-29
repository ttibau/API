# Because we know models don't need
# anything cached from the db into the
# config object it's fine to import it.
from settings import Config as config


class ScoreboardModel:
    def __init__(self, match_data, players: list = None):
        """ match_data expects data given from the match object. """

        self.match_data = match_data
        self.players_list = players

    @property
    def full(self):
        """ Formats and returns full response for scoreboard. """

        self.match_data["players"] = self.players

        return self.match_data

    @property
    def players(self):
        """ Formats players for scoreboard. """

        if not self.players_list:
            raise Exception("Players dict not passed.")

        return_dict = {
            "team_1": {},
            "team_2": {},
            "unassigned": {},
        }

        for player in self.players_list:
            if player["team"] == 1:
                current_team = return_dict["team_1"]
            elif player["team"] == 2:
                current_team = return_dict["team_2"]
            else:
                current_team = return_dict["unassigned"]

            current_team[player["user_id"]] = {
                "name": player["name"],
                "steam_id": player["steam_id"],
                "discord_id": player["discord_id"],
                "joined": player["joined"].strftime(config.timestamp),
                "pfp": config.pfp_cdn.format(player["pfp"]),

                "captain": player["captain"] == 1,
                "alive": player["alive"] == 1,
                "disconnected": player["disconnected"] == 1,
                "ping": player["ping"],
                "mvps": player["mvps"],
                "score": player["mvps"],

                "statistics": {
                    "kills": player["kills"],
                    "headshots": player["headshots"],
                    "assists": player["assists"],
                    "deaths": player["deaths"],
                    "shots_fired": player["shots_fired"],
                    "shots_hit": player["shots_hit"],
                },
            }

        return return_dict
