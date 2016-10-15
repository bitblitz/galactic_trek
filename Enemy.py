import random
from ISectorContent import ISectorContent
import Constants


class Klingon(ISectorContent):
    def __init__(self, coord):
        self.energy = random.randrange(Constants.MIN_ENEMY_ENERGY, Constants.MAX_ENEMY_ENERGY)
        self.coordinate = coord  # create a place to store the coordinate for the object, but don't initialize it yet

    def asChar(self):
        return 'K'
