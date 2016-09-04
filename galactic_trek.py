import abc
import random
import math

# define global variables
g_galaxy = None
g_player = None

GALAXY_SIZE = 10
SECTOR_SIZE = 10
# negative planets are just used to skew the distribution
# and make it less probable there is a planet in any given sector
MIN_PLANETS = -20
MAX_PLANETS = 10
MIN_STARS = 0
MAX_STARS = 6
PROB_BASE = 10  # out of 100
MIN_ENEMY = -5
MAX_ENEMY = 8
MIN_ENEMY_ENERGY = 800
MAX_ENEMY_ENERGY = 1500
PLAYER_INITIAL_ENERGY = 10000
PLAYER_INITIAL_TORPS = 5
PLAYER_MAX_TORPS = 10
PLAYER_INITIAL_SHIELD = 2000
BASE_INITIAL_ENERGY = 100000
BASE_INITIAL_TORPS = 100
BASE_INITIAL_SHIELD = 10000
# Easy start means the first sector will have no enemies
EASY_START = True


class Shape(object):
    @staticmethod
    def asChar():
        """return the single character display letter for the object type"""


class ISectorContent:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def asChar(self):
        return ''


def apply_bound(val, low, high):
    if val < low:
        val = low
    elif val > high:
        val = high
    return val

class Coordinate:
    def __init__(self, r=0, c=0):
        """ stores an integer row and column coordinate for a rectangular coordinate system.
            """
        self.row = r
        self.col = c

    def __repr__(self):
        return 'Coord({self.row}, {self.col})'.format(self=self)

    def __str__(self):
        return '({self.row}, {self.col})'.format(self=self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __mul__(self, other):

        if isinstance(other, (int, float)):
            return Coordinate(self.row * other, self.col * other)
        else:
            return NotImplemented

    def __add__(self, other):

        if isinstance(other, Coordinate):
            return Coordinate(self.row + other.row, self.col + other.col)
        elif isinstance(other, (int, float)):
            return Coordinate(self.row + other, self.col + other)
        else:
            return NotImplemented

    def restrict_to_bounds(self, low, high):
        self.row = apply_bound(self.row, low.row, high.row)
        self.col = apply_bound(self.col, low.col, high.col)
        return self


class Star(ISectorContent):
    def __init__(self, coord):
        self.coordinate = coord

    def asChar(self):
        return '*'


class Enemy(ISectorContent):
    def __init__(self, coord):
        self.energy = random.randrange(MIN_ENEMY_ENERGY, MAX_ENEMY_ENERGY)
        self.coordinate = coord  # create a place to store the coordinate for the object, but don't initialize it yet

    def asChar(self):
        return 'K'


class Planet(ISectorContent):
    def __init__(self, coord):
        self.type = 'M'
        self.coordinate = coord  # create a place to store the coordinate for the object, but don't initialize it yet

    def asChar(self):
        return '+'


class Player(ISectorContent):
    def __init__(self, galaxy):
        self.galaxy = galaxy
        self.energy = PLAYER_INITIAL_ENERGY
        self.torps = PLAYER_INITIAL_TORPS
        self.shield = PLAYER_INITIAL_SHIELD
        # which_sector is the player in?
        self.galaxy_coord = Coordinate(random.randrange(0, GALAXY_SIZE), random.randrange(0, GALAXY_SIZE))

        # place player in galaxy.
        sector = galaxy[self.galaxy_coord]

        # If easy start is set, clear the enemies from the
        # current sector
        if EASY_START:
            sector.enemies.clear()

        # where is the player at, in their current sector? find an empty spot:
        self.sector_coord = sector.map.pickEmpty()
        sector.map[self.sector_coord] = self
        sector.unHide()

    def moveTo(self, gal:Coordinate, sec:Coordinate):
        # leave currect sector
        del self.galaxy[self.galaxy_coord].map[self.sector_coord]
        # move to new sector
        self.galaxy_coord = gal
        sector = self.galaxy[self.galaxy_coord]

        if sec in sector.map:
            # hit something
            print('COLLISSION IMMINENT, EMERGENCY STOP!!')
            sec = sector.map.pickEmpty()

        self.sector_coord = sec
        sector.map[self.sector_coord] = self
        sector.unHide()

    def display(self):
        print('Shield:', self.shield)
        print(' Torps:', self.torps)
        print('Energy:', self.energy)

    def asChar(self):
        return 'P'


class Base(ISectorContent):
    def __init__(self, coord):
        self.energy = BASE_INITIAL_ENERGY
        self.torps = BASE_INITIAL_TORPS
        self.shield = BASE_INITIAL_SHIELD
        self.destroyed = False
        self.coordinate = coord

    def asChar(self):
        return 'B'


# dictionary of occupied coordinates in a sector.  Basically just a dictionary
# with operations to find unoccupied slots (randomly), etc.

class SectorMap(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def ___repr__(self):
        for i in self:
            print(i, self[i])

    def pickEmpty(self):
        while True:
            r = random.randrange(0, SECTOR_SIZE)
            c = random.randrange(0, SECTOR_SIZE)
            # check to see if anything in the sector is already there.
            if Coordinate(r, c) not in self:
                return Coordinate(r, c)


class Sector:
    def __init__(self, row, col):
        self.coordinate = Coordinate(row, col)
        self.hidden = True
        self.bases = list()
        self.map = SectorMap()  # dictionary of occupied spots in Sector
        if random.randint(1, 100) <= PROB_BASE:
            b = Base(self.map.pickEmpty())
            self.bases.append(b)
            self.map[b.coordinate] = b

        # fill the stars list
        self.stars = list()
        for r in range(0, random.randrange(MIN_STARS, MAX_STARS)):
            s = Star(self.map.pickEmpty())
            self.stars.append(s)
            self.map[s.coordinate] = s

        # fill the enemy list
        self.enemies = list()
        for r in range(0, random.randrange(MIN_ENEMY, MAX_ENEMY)):
            e = Enemy(self.map.pickEmpty())
            self.enemies.append(e)
            self.map[e.coordinate] = e

        # fill the planets list
        self.planets = list()
        for r in range(0, random.randrange(MIN_PLANETS, MAX_PLANETS)):
            p = Planet(self.map.pickEmpty())
            self.planets.append(p)
            self.map[p.coordinate] = p

    def unHide(self):
        self.hidden = False

    def print_sector(self):
        for r in range(SECTOR_SIZE):
            for c in range(SECTOR_SIZE):
                coord = Coordinate(r, c)
                if coord in self.map:
                    print(self.map[coord].asChar(), end='')
                else:
                    print('.', end='')
            print('')

        print('-' * SECTOR_SIZE)
        # for i in self.map:
        #    print(i, self.map[i])


class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(GALAXY_SIZE)
        for r in self.size:
            for c in self.size:
                self[Coordinate(r, c)] = Sector(r, c)

    def printRowSep(self,r):
        playerIsRightCol = (g_player.galaxy_coord.col == GALAXY_SIZE-1)
        playerIsThisRow = (r == g_player.galaxy_coord.row)
        playerIsPrevRow = (r == g_player.galaxy_coord.row + 1)
        for c in self.size:
            if c == g_player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                print('************', end='')
            elif c - 1 == g_player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                print('*-----------', end='')
            else:
                print('------------', end='')

        # fill in the last character of the row divider
        if (playerIsThisRow or playerIsPrevRow) and playerIsRightCol:
            print('*')
        else:
            print('-')

    # noinspection PyPep8,PyPep8
    def print(self, showHidden):
        global g_player
        playerIsRightCol = (g_player.galaxy_coord.col == GALAXY_SIZE-1)
        playerIsPrevRow = (g_player.galaxy_coord.row == GALAXY_SIZE - 1)
        playerIsThisRow = False
        playerIsPrevRow = False
        for r in self.size:
            playerIsThisRow = (r == g_player.galaxy_coord.row)
            playerIsPrevRow = (r == g_player.galaxy_coord.row + 1)

            # draw top border
            self.printRowSep(r)

            # print top data row for sector
            for c in self.size:
                if (r == g_player.galaxy_coord.row or (c == g_player.galaxy_coord.col - 1)) and playerIsThisRow:
                    print('* ', end='')
                else:
                    print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    print('s:', len(s.stars), 'e:', len(s.enemies), sep=' ', end=' ')
                else:
                    print('s:', '-', 'e:', '-', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                print('*', end='')
            else:
                print('|', end='')

            print('')
            for c in self.size:
                if (r == g_player.galaxy_coord.row or (c == g_player.galaxy_coord.col - 1)) and playerIsThisRow:
                    print('* ', end='')
                else:
                    print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    print('b:', len(s.bases), 'p:', len(s.planets), sep=' ', end=' ')
                else:
                    print('s:', '-', 'e:', '-', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                print('*', end='')
            else:
                print('|', end='')

            print('')

        # draw bottom
        self.printRowSep(GALAXY_SIZE)


def draw_current_sector():
    print('Current Sector: ', g_player.galaxy_coord)
    g_galaxy[g_player.galaxy_coord].print_sector()
    g_player.display()


def num_input(prompt, low, high):
    val = 0
    while True:
        number = input(prompt)

        try:
            val = int(number)
            if val < low or val > high:  # if not a positive int print message and ask for input again
                print("Invalid Value, try again!")
                continue
            break
        except ValueError:
            print("That's not a number!")
    return val


def convert_direction(direction):
    # convert map direction (0 degrees = up) to trigonometric angle (0 = +x direction, 90 = up)
    # assumes direction is in [0-360]
    # returns radians
    assert 0 <= direction <= 360, "invalid direction conversion"

    theta = 90 - direction
    if theta < 0:
        theta += 360

    return math.radians(theta)


def abs_ceil(x):
    # truncate value towards 
    if x < 0:
        x = math.floor(x)
    else:
        x = math.ceil(x)
    return x


def calc_move_offsets(direction, warp_factor):
    # while the user perceives the galaxy as GALAXY_SIZE sectors of SECTOR_SIZE, logically the
    # galaxy is a flat grid of GALAXY_SIZE * SECTOR_SIZE coordinates across, so we calculate moves in global
    # coordinates.
    # one warp_factor is equivalent to exactly one SECTOR_SIZE of global coordinates.
    theta = convert_direction(direction)
    x = math.trunc(warp_factor * SECTOR_SIZE * math.cos(theta))
    y = -math.trunc(warp_factor * SECTOR_SIZE * math.sin(theta))

    return Coordinate(y, x)


def galsec_to_global(gal: Coordinate, sec: Coordinate) -> Coordinate:
    # convert galactic/sector coord pair to global coordinate
    return gal * SECTOR_SIZE + sec


def global_to_galsec(global_coord):
    # convert galactic/sector coord pair to global coordinate
    gal = Coordinate(int(global_coord.row / SECTOR_SIZE), int(global_coord.col / SECTOR_SIZE))
    sec = global_coord + (gal * -SECTOR_SIZE)
    return gal, sec


def calc_global_move(delta, gal_coord, sector_coord):
    gl = galsec_to_global(gal_coord, sector_coord)
    #print('global1:', gl)
    #print('delta:', delta)
    gl += delta
    gl.restrict_to_bounds(Coordinate(0,0), Coordinate(GALAXY_SIZE*SECTOR_SIZE-1, GALAXY_SIZE*SECTOR_SIZE-1))
    #print('global2:', gl)
    #print('global2gs:',  global_to_galsec(gl))

    return global_to_galsec(gl)


def Warp(player):
    direction = num_input('Warp Direction (0-359 degrees, 0 = up)?', 0, 360)
    factor = num_input('Warp Factor (1-9)?', 1, 9)

    delta = calc_move_offsets(direction, factor)

    # calculate the new coordinates from the global ones
    gal_coord, sec_coord = calc_global_move(delta, player.galaxy_coord, player.sector_coord)

    #print('moving from :G:', player.galaxy_coord, ':S:', player.sector_coord)
    #print('Delta', delta)
    #print('moving   to :G:', gal_coord, ':S:', sec_coord)
    # pause
    #input()
    player.moveTo(gal_coord, sec_coord)


def process_command(cmd):
    global g_player
    global g_galaxy

    cmd = cmd.upper()
    if cmd == 'W':
        Warp(g_player)
    elif cmd == 'I':
        # Impulse(g_player)
        pass
    elif cmd == 'G':
        g_galaxy.print(False);
    else:
        print('invalid cmd:', cmd)


# noinspection PyAugmentAssignment
def tests():
    #print('running tests')
    # check some basic coordinate conversions
    gal = Coordinate(1, 2)
    sec = Coordinate(3, 4)
    gl = galsec_to_global(gal, sec)
    assert gl.row == gal.row * SECTOR_SIZE + sec.row
    assert gl.col == gal.col * SECTOR_SIZE + sec.col
    g2, s2 = global_to_galsec(gl)
    assert gal == g2
    assert sec == s2
    gal = gal * 3
    assert gal.row == 3 and gal.col == 6
    sec += Coordinate(-1, -3)
    assert sec.row == 2 and sec.col == 1


# main code
def main():
    global g_galaxy
    global g_player
    # initialize game
    random.seed(1)
    g_galaxy = Galaxy()
    g_player = Player(g_galaxy)
    g_galaxy.print(False)
    tests()

    # main loop
    while True:
        draw_current_sector()
        cmd = input('(W)arp, (I)mpulse, (G)alaxy Map:')
        process_command(cmd)

if __name__ == '__main__':
    main()

