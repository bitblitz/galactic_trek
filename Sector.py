from Base import Base
import Enemy
from Planet import Planet
from SectorMap import *
from Star import Star
import Drawing


class Sector:
    def __init__(self, row, col):
        self.coordinate = Coordinate(row, col)
        self.map = SectorMap()  # dictionary of occupied spots in Sector
        self.bases = list()
        self.klingons = list()
        self.otherEnemies = list()
        self.planets = list()

        # every sector has at least one star, initially
        self.stars = list()
        for i in range(random.randint(1, 9)):
            self.addStar()

    def addBase(self):
        b = Base(self.map.pickEmpty())
        self.bases.append(b)
        self.map[b.coordinate] = b

    def addKlingon(self):
        e = Enemy.Klingon(self.map.pickEmpty())
        self.klingons.append(e)
        self.map[e.coordinate] = e

    def addPlanet(self):
        p = Planet(self.map.pickEmpty())
        self.planets.append(p)
        self.map[p.coordinate] = p

    def addStar(self):
        s = Star(self.map.pickEmpty())
        self.stars.append(s)
        self.map[s.coordinate] = s

        # clear enemies from current sector
        # def clearEnemies(self):
        #    # clear enemies from map
        #    for e in self.enemies:
        #        del self.map[e.coordinate]

        # and remove them all

    #    self.enemies.clear()


    def print_sector(self, left, top):
        lineator = Drawing.Lineator(left, top)
        lineator.print(
            "{:>2}{:^3}{:^3}{:^3}{:^3}{:^3}{:^3}{:^3}{:^3}{:^3}{:^3}".format(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        for r in range(Constants.SECTOR_SIZE):
            lineator.print("{:>2}".format(r + 1), end='')
            for c in range(Constants.SECTOR_SIZE):
                coord = Coordinate(r, c)
                if coord in self.map:
                    lineator.print(' ', self.map[coord].asChar(), ' ', sep='', end='')
                else:
                    lineator.print(' . ', sep='', end='')
            lineator.print('')

        lineator.drawBoundingRect(fill='purple', outline='yellow', background=True)
        return lineator.bbox
