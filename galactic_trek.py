import abc
import random
from Coordinate import *
from UserInput import num_input, queue_input, command_input

import Constants
import UserInput

# define global variables
g_galaxy = None
g_player = None


class ISectorContent:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def asChar(self):
        """return the single character display letter for the object type"""
        return ''


class Star(ISectorContent):
    def __init__(self, coord):
        self.coordinate = coord

    def asChar(self):
        return '*'


class Enemy(ISectorContent):
    def __init__(self, coord):
        self.energy = random.randrange(Constants.MIN_ENEMY_ENERGY, Constants.MAX_ENEMY_ENERGY)
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
        self.energy = Constants.PLAYER_INITIAL_ENERGY
        self.torps = Constants.PLAYER_INITIAL_TORPS
        self.shield = Constants.PLAYER_INITIAL_SHIELD
        # which_sector is the player in?
        self.galaxy_coord = Coordinate(random.randrange(0, Constants.GALAXY_SIZE),
                                       random.randrange(0, Constants.GALAXY_SIZE))

        # place player in galaxy.
        sector = galaxy[self.galaxy_coord]

        # If easy start is set, clear the enemies from the
        # current sector
        if Constants.EASY_START:
            sector.enemies.clear()

        # where is the player at, in their current sector? find an empty spot:
        self.sector_coord = sector.map.pickEmpty()
        sector.map[self.sector_coord] = self
        sector.unHide()

    def alert(message, soundId):
        print(message, "Sound: " + soundId)


    def move(self, delta, energy_cost):

        if energy_cost > self.energy:
            self.alert("Not enough energy for that!", Constants.ERROR_SOUND)
        else:
            self.energy -= energy_cost

            # calculate the new coordinates from the global ones
            (gal_coord, sec_coord) = calc_global_move(delta, self.galaxy_coord, self.sector_coord)
            # debug_print('moving from :G:', player.galaxy_coord, ':S:', player.sector_coord)
            # debug_print('Delta', delta)
            # debug_print('moving   to :G:', gal_coord, ':S:', sec_coord)
            self.moveTo(gal_coord, sec_coord)

    def moveTo(self, gal: Coordinate, sec: Coordinate):
        # leave current sector
        del self.galaxy[self.galaxy_coord].map[self.sector_coord]
        # move to new sector
        self.galaxy_coord = gal
        sector = self.galaxy[self.galaxy_coord]

        if sec in sector.map:
            # hit something
            self.alert('COLLISION IMMINENT, EMERGENCY STOP!!', Constants.ALERT_SOUND)
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
        self.energy = Constants.BASE_INITIAL_ENERGY
        self.torps = Constants.BASE_INITIAL_TORPS
        self.shield = Constants.BASE_INITIAL_SHIELD
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
            r = random.randrange(0, Constants.SECTOR_SIZE)
            c = random.randrange(0, Constants.SECTOR_SIZE)
            # check to see if anything in the sector is already there.
            if Coordinate(r, c) not in self:
                return Coordinate(r, c)


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


class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)
        for r in self.size:
            for c in self.size:
                self[Coordinate(r, c)] = Sector(r, c)

    def printRowSep(self, r):
        playerIsRightCol = (g_player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
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
        playerIsRightCol = (g_player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        # playerIsPrevRow = (g_player.galaxy_coord.row == Constants.GALAXY_SIZE - 1)
        # playerIsThisRow = False
        # playerIsPrevRow = False
        for r in self.size:
            playerIsThisRow = (r == g_player.galaxy_coord.row)
            # playerIsPrevRow = (r == g_player.galaxy_coord.row + 1)

            # draw top border
            self.printRowSep(r)

            # print top data row for sector
            for c in self.size:
                if playerIsThisRow and (c == g_player.galaxy_coord.col or c-1 == g_player.galaxy_coord.col):
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
            # print second row
            for c in self.size:
                if playerIsThisRow and (c == g_player.galaxy_coord.col or c-1 == g_player.galaxy_coord.col):
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
        self.printRowSep(Constants.GALAXY_SIZE)


def draw_current_sector():
    print('Current Sector: ', g_player.galaxy_coord)
    g_galaxy[g_player.galaxy_coord].print_sector()
    g_player.display()


def Warp(player):
    direction = num_input('Warp Direction (0-359 degrees, 0 = up)', 0, 360)
    factor = num_input('Warp Factor (1-9)', 1, 9)

    (delta, energy_cost) = calc_move_offsets(direction, factor)
    player.move(delta, energy_cost)


def Impulse(player):
    direction = num_input('Warp Direction (0-359 degrees, 0 = up)', 0, 360)
    factor = num_input('Impulse Factor (1-9)', 1, 9)

    (delta, energy_cost) = calc_move_offsets(direction, factor / 10)
    player.move(delta, energy_cost)


def process_command(cmd):
    global g_player
    global g_galaxy

    cmd = cmd.upper()
    if cmd == 'W':
        Warp(g_player)
    elif cmd == 'I':
        Impulse(g_player)
    elif cmd == 'G':
        g_galaxy.print(False)
    else:
        print('invalid cmd:', cmd)



# main code
def main():
    global g_galaxy
    global g_player
    # initialize game
    random.seed(1)
    g_galaxy = Galaxy()
    g_player = Player(g_galaxy)
    g_galaxy.print(False)
    queue_input([ "w", "270", "2", "g"])

    # main loop
    while True:
        draw_current_sector()
        cmd = command_input()
        process_command(cmd)


if __name__ == '__main__':
    main()
