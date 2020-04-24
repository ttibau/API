import uuid

from random import shuffle
from discord.utils import escape_markdown

class Misc(object):
    def uuid4():
        """ Returns string version of uuid.uuid4(). """
        return str(uuid.uuid4())

    def list_random(given_list: list):
        """ Randomizes the list. """
        return shuffle(given_list)

    def sanitation(given_string: str, limit=13):
        """ Sanitation for discord markdown and inforces a string limit. """

        if len(given_string) > 12:
            given_string = given_string[:12]

        given_string = escape_markdown(given_string)

        return given_string