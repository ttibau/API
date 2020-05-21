from random import shuffle


class Map:
    def __init__(self, details, maps):
        self.details = details
        self.maps = maps

    def given(self):
        """ Sets the map as the 1st index in the given maps. """

        self.details["map"] = self.maps["list"][0]
        self.details["map_order"] = None

    def random(self):
        """ Sets a random map from the given maps. """

        shuffle(self.maps)

        self.details["map"] = self.maps["list"][0]
        self.details["map_order"] = None

    def veto(self):
        """ Sets map selection type to veto. """

        self.details["map"] = None
        self.details["map_order"] = self.maps["options"]["selection"]
