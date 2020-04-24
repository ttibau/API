from random import shuffle

class Map(object):
    def __init__(self, obj):
        self.obj = obj

    def given(self):
        """ Sets the map as the 1st index in the given maps. """

        self.obj.data["details"]["map"] = self.obj.maps[0]

    def random(self):
        """ Sets a random map from the given maps. """

        shuffle(self.obj.maps)
        self.obj.data["details"]["map"] = self.obj.maps[0]

    def veto(self):
        """ Sets map selection type to veto. """

        self.obj.data["details"]["map"] = None

    def vote(self):
        """ Sets map selection type to veto. """

        self.obj.data["details"]["map"] = None