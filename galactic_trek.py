import random

GALAXY_SIZE=10
SECTOR_SIZE=10
# negative planets are just used to skew the distribution
# and make it less probable there is a planet in any given sector
MIN_PLANETS=-20
MAX_PLANETS=10
MIN_STARS = 0
MAX_STARS = 6
PROB_BASE = 10 # out of 100
MIN_ENEMY = -5
MAX_ENEMY = 8
MIN_ENEMY_ENERGY = 800
MAX_ENEMY_ENERGY = 1500
PLAYER_INITIAL_ENERGY = 10000
PLAYER_INITIAL_TORPS  = 5
PLAYER_MAX_TORPS = 10
PLAYER_INITIAL_SHIELD = 2000
BASE_INITIAL_ENERGY = 100000
BASE_INITIAL_TORP   = 100
BASE_INITIAL_SHIELD = 10000
# Easy start means the first sector will have no enemies
EASY_START= True

import abc

class Shape(object):
    def asChar(self):
        """return the single character display letter for the object type"""

class ISectorContent:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def asChar(self):
        return ''

class Coordinate:
    def __init__(self, r=-1, c=-1):
        """ stores an integer row and column coordinate for a rectangular coordinate system.
            -1 means not initialized """
        self.row = r;
        self.col = c;

    def __repr__(self):
        return 'Coord({self.row}, {self.col})'.format(self=self)

    def __str__(self):
        return '({self.row}, {self.col})'.format(self=self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def isSet():
        return self.row >= 0 and self.col >= 0

class Star(ISectorContent):
    def __init__(self, coord):
        self.coordinate = coord;

    def asChar(self):
        return '*'

class Enemy(ISectorContent):
    def __init__(self, coord):
        self.energy=random.randint(MIN_ENEMY_ENERGY, MAX_ENEMY_ENERGY);
        self.coordinate = coord # create a place to store the coordinate for the object, but don't initialize it yet

    def asChar(self):
        return 'K'

class Planet(ISectorContent):
    def __init__(self, coord):
        self.type='M'
        self.coordinate = coord # create a place to store the coordinate for the object, but don't initialize it yet
    def asChar(self):
        return '+'

class Player(ISectorContent):
    def __init__(self, galaxy):
        self.energy = PLAYER_INITIAL_ENERGY;
        self.torps  = PLAYER_INITIAL_TORPS;
        self.shield = PLAYER_INITIAL_SHIELD;
        # which_sector is the player in?
        self.galaxy_coord = Coordinate(random.randrange(0, GALAXY_SIZE), random.randrange(0, GALAXY_SIZE))

        # place player in galaxy. 
        sector = galaxy[self.galaxy_coord]
        
        #If easy start is set, clear the enemies from the
        # current sector
        if EASY_START:
            sector.enemies.clear()
            
        # where is the player at, in their current sector? find an empty spot:
        self.sector_coord = sector.map.pickEmpty()
        sector.map[self.sector_coord]= self
        sector.unhide()

    def asChar(self):
        return 'P'

class Base(ISectorContent):
    def __init__(self, coord):
        self.energy = BASE_INITIAL_ENERGY
        self.torps  = BASE_INITIAL_TORP
        self.shield = BASE_INITIAL_SHIELD
        self.destroyed = False
        self.coordinate = coord

    def asChar(self):
        return 'B'

# dictionary of occupied coordinates in a sector.  Basically just a dictionary
# with operations to find unoccupied slots (randomly), etc.

class SectorMap(dict):
    def __init__(self):
        pass

    def ___repr__(self):
        for i in self:
            print( i, self[i] )

    def pickEmpty(self):
        while True:
            r = random.randrange(0, SECTOR_SIZE)
            c = random.randrange(0, SECTOR_SIZE)
            # check to see if anything in the sector is already there.
            if Coordinate(r,c) not in self:
                return Coordinate(r,c)


class Sector:
    def __init__(self, row, col):
        self.coordinate = Coordinate(row,col)
        self.hidden = True
        self.bases = list();
        self.map = SectorMap(); # dictionary of occupied spots in Sector
        if random.randint(1,100) <= PROB_BASE:
            b = Base(self.map.pickEmpty())
            self.bases.append(b)
            self.map[b.coordinate]=b

        # fill the stars list
        self.stars = list()
        for r in range(0,random.randint(MIN_STARS, MAX_STARS)):
            s = Star(self.map.pickEmpty())
            self.stars.append(s)
            self.map[s.coordinate]=s

        # fill the enemy list
        self.enemies=list();
        for r in range(0,random.randint(MIN_ENEMY, MAX_ENEMY)):
            e = Enemy(self.map.pickEmpty())
            self.enemies.append(e)
            self.map[e.coordinate]=e

        # fill the planets list
        self.planets= list();
        for r in range(0,random.randint(MIN_PLANETS, MAX_PLANETS)):
            p = Planet(self.map.pickEmpty())
            self.planets.append(p)
            self.map[p.coordinate]=p

    def unhide(self):
        self.hidden = False

    def print_sector(self):
        for r in range(SECTOR_SIZE):
            for c in range(SECTOR_SIZE):
                coord = Coordinate(r,c)
                if coord in self.map:
                    print(self.map[coord].asChar(),end='')
                else:
                    print('.', end='')
            print('\n')

        print( '-' * SECTOR_SIZE )
        #for i in self.map:
        #    print(i, self.map[i])

class Galaxy(dict):
    def __init__(self):
        self.size = range(GALAXY_SIZE)
        for r in self.size:
            for c in self.size:
                self[Coordinate(r,c)] = Sector(r,c);


    def print(self, showHidden):
        print('-------------------------------------------------------------------------------------------------------------------------\r');
        for r in self.size:
            print('| ', end='');
            for c in self.size:
                s = self[Coordinate(r,c)]
                if showHidden or not s.hidden:
                    print( 's:', len(s.stars) , 'e:' , len(s.enemies), sep=' ', end=' | ');
                else:
                    print( 's:', '-' , 'e:' , '-', sep=' ', end=' | ');
            print('\r')
            print('| ', end='');
            for c in self.size:
                s = self[Coordinate(r,c)]
                if showHidden or not s.hidden:
                    print( 'b:', len(s.bases) , 'p:' , len(s.planets), sep=' ', end=' | ');
                else:
                    print( 's:', '-' , 'e:' , '-', sep=' ', end=' | ');
            print('\r');
            print('-------------------------------------------------------------------------------------------------------------------------\r');

            #for c in self.size:
            #    s = self[Coordinate(r,c)]
            #    print('Sector:' + str(s.coordinate));
            #    s.print_sector()

    

# main code
random.seed(1)
g_galaxy = Galaxy()
g_player= Player(g_galaxy)
g_galaxy.print(False);
print('Current Sector: ', g_player.galaxy_coord)
g_galaxy[g_player.galaxy_coord].print_sector()
