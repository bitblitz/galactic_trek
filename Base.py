import Constants
from ISectorContent import ISectorContent


class Base(ISectorContent):
    def __init__(self, coord):
        self.energy = Constants.BASE_INITIAL_ENERGY
        self.torps = Constants.BASE_INITIAL_TORPS
        self.shield = Constants.BASE_INITIAL_SHIELD
        self.destroyed = False
        self.coordinate = coord

    def asChar(self):
        return 'B'
