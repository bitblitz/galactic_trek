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
MAX_ENEMY = 10
MIN_ENEMY_ENERGY = 800
MAX_ENEMY_ENERGY = 1500
PLAYER_INITIAL_ENERGY = 10000
PLAYER_INITIAL_TORPS  = 5
PLAYER_MAX_TORPS = 10
PLAYER_INITIAL_SHIELD = 2000
BASE_INITIAL_ENERGY = 100000
BASE_INITIAL_TORP   = 100
BASE_INITIAL_SHIELD = 10000

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
        return 'E'        
        
class Planet(ISectorContent):
    def __init__(self, coord):
        self.type='M'
        self.coordinate = coord # create a place to store the coordinate for the object, but don't initialize it yet
    def asChar(self):
        return '+'        

class Player(ISectorContent):
    def __init__(self):
        self.energy = PLAYER_INITIAL_ENERGY;
        self.torps  = PLAYER_INITIAL_TORPS;
        self.shield = PLAYER_INITIAL_SHIELD;
        # which_sector is the player in?
        self.sector_number = Coordinate(random.randint(0, GALAXY_SIZE), random.randint(0, GALAXY_SIZE))
        # where is the player at, in their current sector?
        self.coordinate = Coordinate()

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

    def pickEmpty(self):
        while True:
            r = random.randint(1, SECTOR_SIZE)
            c = random.randint(1, SECTOR_SIZE)
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
        for r in range(1,random.randint(MIN_STARS, MAX_STARS)):
            s = Star(self.map.pickEmpty())
            self.stars.append(s)
            self.map[s.coordinate]=s
                       
        # fill the enemy list
        self.enemies=list();
        for r in range(1,random.randint(MIN_ENEMY, MAX_ENEMY),1):
            e = Enemy(self.map.pickEmpty())
            self.enemies.append(e)
            self.map[e.coordinate]=e

        # fill the planets list
        self.planets= list();
        for r in range(1,random.randint(MIN_PLANETS, MAX_PLANETS),1):
            p = Enemy(self.map.pickEmpty())
            self.planets.append(p)
            self.map[p.coordinate]=p
  
        self.generate_sector_map()

    # arrange the sector contents    
    def generate_sector_map(sector):
        pass

    def print_sector(self):
        for r in range(SECTOR_SIZE):
            for c in range(SECTOR_SIZE):
                coord = Coordinate(r,c)
                if coord in self.map:
                    print(self.mamp[coord].asChar(),end='')
                else:
                    print('.', end='')
            print('\n')
        print('\n')
        
            
def generate_galaxy():
    galaxy = list(); # galaxy is a list of lists of GALAXY_SIZE;
    for r in range(GALAXY_SIZE):
        # create the row of sectors
        row = list()
        # initialize each sector:
        for s in range(GALAXY_SIZE):
            row.append( Sector(r, s) );

        galaxy.append(row);

    return galaxy;

def print_galaxy(galaxy, showHidden):
    print('-------------------------------------------------------------------------------------------------------------------------\r');
    for r in galaxy:
        print('| ', end='');
        for s in r:
            if showHidden or not s.hidden:
                print( 's:', len(s.stars) , 'e:' , len(s.enemies), sep=' ', end=' | ');
            else:
                print( 's:', '-' , 'e:' , '-', sep=' ', end=' | ');
        print('\r')
        print('| ', end='');
        for s in r:
            if showHidden or not s.hidden:
                print( 'b:', len(s.bases) , 'p:' , len(s.planets), sep=' ', end=' | ');
            else:
                print( 's:', '-' , 'e:' , '-', sep=' ', end=' | ');
        print('\r');
        print('-------------------------------------------------------------------------------------------------------------------------\r');


        for s in r:
            print('Sector:' + str(s.coordinate));
            s.print_sector()
            print('----')
    
# main code
g_galaxy = generate_galaxy();
print_galaxy(g_galaxy, True);

        

    
