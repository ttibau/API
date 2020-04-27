from models.match import MatchModel

class ScoreboardModel:
    def __init__(self, match: dict = None, players: dict = None):
        self.match = match
        self.players = players

    @property
    def full(self):
        """ Formats and returns full response for scoreboard. """

        return {
            **self.minimal,
            "players": self.players,
        }

    @property
    def minimal(self):
        """ Scoreboard minimal. """

        if not self.match:
            raise Exception("Match dict not passed.")
        
        return MatchModel(self.match).full

    @property
    def players(self):
        """ Formats players for scoreboard. """

        if not self.players:
            raise Exception("Players dict not passed.")

        return_dict = {
            "team_1": [],
            "team_2": [],
            "spectator": [],
        }

        team_1_append = return_dict["team_1"].append
        team_2_append = return_dict["team_2"].append
        spectator_append = return_dict["spectator"].append

        for player in self.players:
            if player["team"] == 1:
                team_append = team_1_append
            elif player["team"] == 2:
                team_append = team_2_append
            else:
                team_append = spectator_append

            team_append({
                "user_id": player["user_id"],
                "name": player["name"],
                "steam_id": player["steam_id"],
                "discord_id": player["discord_id"],
                "joined": player["joined"],
                "pfp": player["pfp"],

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
            })

        return return_dict