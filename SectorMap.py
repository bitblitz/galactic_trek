import random
import Constants
from Coordinate import Coordinate


class SectorMap(dict):
    # dictionary of occupied coordinates in a sector.  Basically just a dictionary
    # with operations to find unoccupied slots (randomly), etc.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def ___repr__(self):
        for i in self:
            print(i, self[i])

    def pickEmpty(self):
        while True:
            r = random.randrange(0, Constants.SECTOR_SIZE)
            c = random.randrange(0, Constants.SECTOR_SIZE)
            # check to see if anything in the sector is already there.
            if Coordinate(r, c) not in self:
                return Coordinate(r, c)
