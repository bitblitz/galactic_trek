import random
from ISectorContent import ISectorContent
from Coordinate import *
from Galaxy import Galaxy
import StarChart
import Drawing
import IGameStage
from ActiveGame import ActiveGame

class Player(ISectorContent):
    def __init__(self, game:ActiveGame, galaxy: Galaxy):
        self.parent_galaxy = galaxy
        self.game = game
        self.energy = Constants.PLAYER_INITIAL_ENERGY
        self.torps = Constants.PLAYER_INITIAL_TORPS
        self.shield = Constants.PLAYER_INITIAL_SHIELD
        # which_sector is the player in?
        self.galaxy_coord = Coordinate(random.randrange(0, Constants.GALAXY_SIZE),
                                       random.randrange(0, Constants.GALAXY_SIZE))

        # place player in galaxy.
        self.sector = galaxy[self.galaxy_coord]
        self.handicap = 1

        # where is the player at, in their current sector? find an empty spot:
        self.sector_coord = self.sector.map.pickEmpty()
        self.sector.map[self.sector_coord] = self

        self.brigCapacity = 400
        self.captured_klingons = 0
        self.cloak_violations = 0
        self.is_cloaked = False
        self.is_cloaking = False
        # star chart is a partial display of galaxy contents, but
        # uses the same class, so create an empty one
        self.starChart = StarChart.StarChart()
        self.starChart.updateFromSector(self.sector)

    @staticmethod
    def dock(base):
        print('Docking...')

    def move(self, delta, energy_cost):

        if energy_cost > self.energy:
            self.game.alertUser("Not enough energy for that!", Constants.ERROR_SOUND)
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
        del self.parent_galaxy[self.galaxy_coord].map[self.sector_coord]
        # move to new sector
        self.galaxy_coord = gal
        self.sector = self.parent_galaxy[self.galaxy_coord]

        if sec in self.sector.map:
            # hit something
            self.game.alertUser('COLLISION IMMINENT, EMERGENCY STOP!!', Constants.ALERT_SOUND)
            sec = self.sector.map.pickEmpty()

        self.sector_coord = sec
        self.sector.map[self.sector_coord] = self
        self.starChart.updateFromSector(self.sector)

    def display_status(self, left, top, game):
        hasEnemies = not not self.sector.klingons
        if hasEnemies:
            condition = "RED!"
        elif self.energy < Constants.YELLOW_ALERT_ENERGY:
            condition = "Yellow"
        else:
            condition = "Green"

        lineator = Drawing.Lineator(left, top)
        lineator.print('   Star Date:', game.stardate/100)
        lineator.print('   Condition:', condition)
        lineator.print('    Position:', self.galaxy_coord, '@', self.sector_coord)
        lineator.print('Life Support:', 'ACTIVE')
        lineator.print(' Warp Factor:', 'N/A')
        lineator.print('       Torps:', self.torps)
        lineator.print('      Energy:', self.energy)
        lineator.print('      Shield:', self.shield)
        lineator.print('    Klingons:', game.cur_klingons+game.cur_commanders+game.cur_superCommanders)
        lineator.print('        Time:', game.remaining_time)
        return lineator.bbox

    def asChar(self):
        return 'E'
