import random
from ISectorContent import ISectorContent
from Coordinate import *


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

    @staticmethod
    def alertUser(message, soundId):
        print(message, "Sound: " + soundId)

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
        sector = self.galaxy[self.galaxy_coord]

        if sec in sector.map:
            # hit something
            self.alertUser('COLLISION IMMINENT, EMERGENCY STOP!!', Constants.ALERT_SOUND)
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
