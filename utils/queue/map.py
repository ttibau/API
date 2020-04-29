from random import shuffle


class Map(object):
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

        # Decided to keep veto and vote seperate functions in case if each
        # type needs some different functionality later on.

        self.obj.details["map"] = None
        self.obj.details["map_order"] = self.obj.selection_types[
            self.obj.maps["options"]["selection"]
        ]

    def vote(self):
        """ Sets map selection type to vote. """

        self.obj.details["map"] = None
        self.obj.details["map_order"] = self.obj.selection_types[
            self.obj.maps["options"]["selection"]
        ]
