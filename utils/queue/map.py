from random import shuffle


class Map:
    def __init__(self, obj):
        self.obj = obj

    def given(self):
        """ Sets the map as the 1st index in the given maps. """

        self.obj.details["map"] = self.obj.maps["list"][0]
        self.obj.details["map_order"] = None

    def random(self):
        """ Sets a random map from the given maps. """

        shuffle(self.obj.maps["list"])

        self.obj.details["map"] = self.obj.maps["list"][0]
        self.obj.details["map_order"] = None

    def veto(self):
        """ Sets map selection type to veto. """

        self.obj.details["map"] = None
        self.obj.details["map_order"] = self.obj.maps["options"]["selection"]
