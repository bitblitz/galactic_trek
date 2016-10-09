import random
from ISectorContent import ISectorContent
from Coordinate import *
from Galaxy import Galaxy
import Drawing


class Player(ISectorContent):
    def __init__(self, galaxy: Galaxy):
        self.galaxy = galaxy
        self.energy = Constants.PLAYER_INITIAL_ENERGY
        self.torps = Constants.PLAYER_INITIAL_TORPS
        self.shield = Constants.PLAYER_INITIAL_SHIELD
        # which_sector is the player in?
        self.galaxy_coord = Coordinate(random.randrange(0, Constants.GALAXY_SIZE),
                                       random.randrange(0, Constants.GALAXY_SIZE))

        # place player in galaxy.
        self.sector = galaxy[self.galaxy_coord]

        # If easy start is set, clear the enemies from the
        # current sector
        if Constants.EASY_START:
            self.sector.enemies.clear()

        # where is the player at, in their current sector? find an empty spot:
        self.sector_coord = self.sector.map.pickEmpty()
        self.sector.map[self.sector_coord] = self
        self.sector.unHide()

    @staticmethod
    def alertUser(message, soundId):
        print(message, "Sound: ", soundId)

    @staticmethod
    def dock(base):
        print('Docking...')

    def move(self, delta, energy_cost):

        if energy_cost > self.energy:
            self.alertUser("Not enough energy for that!", Constants.ERROR_SOUND)
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
        self.sector = self.galaxy[self.galaxy_coord]

        if sec in self.sector.map:
            # hit something
            self.alertUser('COLLISION IMMINENT, EMERGENCY STOP!!', Constants.ALERT_SOUND)
            sec = self.sector.map.pickEmpty()

        self.sector_coord = sec
        self.sector.map[self.sector_coord] = self
        self.sector.unHide()

    def display_status(self, left, top):
        lineator = Drawing.Lineator(left, top)
        lineator.print('   Shield:', self.shield)
        lineator.print('    Torps:', self.torps)
        lineator.print('   Energy:', self.energy)
        hasEnemies = not not self.galaxy[self.galaxy_coord].enemies
        if hasEnemies:
            condition = "RED!"
        elif self.energy < Constants.YELLOW_ALERT_ENERGY:
            condition = "Yellow"
        else:
            condition = "Green"

        lineator.print('Condition:', condition)

    def asChar(self):
        return 'E'
