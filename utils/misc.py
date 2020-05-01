import uuid

from discord.utils import escape_markdown


class Misc:
    def uuid4():
        """ Returns string version of uuid.uuid4(). """
        return str(uuid.uuid4())

    def sanitation(given_string: str, limit=13):
        """ Sanitation for discord markdown and inforces a string limit. """

        if len(given_string) > 12:
            given_string = given_string[:13]

        given_string = escape_markdown(given_string)

        return given_string

    def determine_winner(team_1: dict, team_2: dict):
        """ Expects teams passed from match model. """

        if team_1["score"] == team_2["score"]:
            return "tie"

        total_rounds = team_1["score"] + team_2["score"]
        amount_to_win = total_rounds / 2

        if team_1["score"] >= amount_to_win:
            return "team_1"
        else:
            return "team_2"
