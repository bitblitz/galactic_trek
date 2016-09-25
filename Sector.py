from Base import Base
from Enemy import Enemy
from Planet import Planet
from SectorMap import *
from Star import Star


class Sector:
    def __init__(self, row, col):
        self.coordinate = Coordinate(row, col)
        self.hidden = True
        self.bases = list()
        self.map = SectorMap()  # dictionary of occupied spots in Sector
        if random.randint(1, 100) <= Constants.PROB_BASE:
            b = Base(self.map.pickEmpty())
            self.bases.append(b)
            self.map[b.coordinate] = b

        # fill the stars list
        self.stars = list()
        for r in range(0, random.randrange(Constants.MIN_STARS, Constants.MAX_STARS)):
            s = Star(self.map.pickEmpty())
            self.stars.append(s)
            self.map[s.coordinate] = s

        # fill the enemy list
        self.enemies = list()
        for r in range(0, random.randrange(Constants.MIN_ENEMY, Constants.MAX_ENEMY)):
            e = Enemy(self.map.pickEmpty())
            self.enemies.append(e)
            self.map[e.coordinate] = e

        # fill the planets list
        self.planets = list()
        for r in range(0, random.randrange(Constants.MIN_PLANETS, Constants.MAX_PLANETS)):
            p = Planet(self.map.pickEmpty())
            self.planets.append(p)
            self.map[p.coordinate] = p

    def unHide(self):
        self.hidden = False

    def print_sector(self):
        for r in range(Constants.SECTOR_SIZE):
            for c in range(Constants.SECTOR_SIZE):
                coord = Coordinate(r, c)
                if coord in self.map:
                    print(self.map[coord].asChar(), end='')
                else:
                    print('.', end='')
            print('')

        print('-' * Constants.SECTOR_SIZE)
        # for i in self.map:
        #    print(i, self.map[i])
