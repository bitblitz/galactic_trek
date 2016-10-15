import Constants
import random
from Coordinate import Coordinate
from Sector import Sector


# Galaxy is the container of all sectors in the galaxy and represents the entire galaxy state.
class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)

    def randomSector(self) -> Sector:
        r = random.randint(0, Constants.GALAXY_SIZE - 1)
        c = random.randint(0, Constants.GALAXY_SIZE - 1)
        return self[Coordinate(r, c)]
