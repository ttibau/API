class MatchModel:
    def __init__(self, data: dict):
        self.data = data

    @property
    def full(self):
        """ Formats and returns full match response. """

        return {
            **self.minimal,
            "team_1": self.team_1,
            "team_2": self.team_2,
        }

    @property
    def minimal(self):
        """ Formats minimal response. """

        return {
                "match_id": self.data["match_id"],
                "server_id": self.data["server_id"],
                "map": self.data["map"],
                "status": self.data["status"],
                "timestamp": self.data["timestamp"],
                "map_order": self.data["map_order"],
                "player_order": self.data["player_order"],
        }

    @property
    def team_1(self):
        """ Formats team 1 response. """

        return {
                "name": self.data["team_1_name"],
                "score": self.data["team_1_score"],
                "side": self.data["team_1_side"],
        }

    @property
    def team_2(self):
        """ Formats team 2 response. """

        return {
                "name": self.data["team_2_name"],
                "score": self.data["team_2_score"],
                "side": self.data["team_2_side"],
        }