import secrets
import os
import sys


class MasterKey:
    def __init__(self):
        self.pathway = os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            "master_key.txt"
        )

    def load(self):
        """ Attempts to load master key. """

        if os.path.exists(self.pathway):
            with open(self.pathway, mode="r") as file:
                return file.read()
        else:
            return self.generate()

    def generate(self):
        """ Generates master key file with key. """

        key = secrets.token_urlsafe(48)
        with open(self.pathway, mode="w") as file:
            file.write(key)

        return key


MASTER_KEY = MasterKey().load()
