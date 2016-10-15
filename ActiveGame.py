""" One game pass, options, etc. """
import Drawing
from Galaxy import Galaxy
from Sector import Sector
from Player import Player
from Coordinate import *
import UserInput
from Base import Base
import Globals
from IGameStage import IGameStage
import Util
from enum import Enum
import random

_command_prompt = '(W)arp, (I)mpulse, (L)ong Range Scan'


class GameDifficulty(Enum):
    Novice = 1
    Fair = 2
    Good = 3
    Hard = 4
    Impossible = 5


class GameLength(Enum):
    Short = 1
    Medium = 2
    Long = 4


class ActiveGame(IGameStage):
    def __init__(self):
        self.player = Player(self.galaxy)
        self.game_over = False
        # track star dates as intger * 100 (i.e. 3100.01 = 310001
        self.difficulty = GameDifficulty.Novice
        self.gameLength = GameLength.Medium
        self.initial_stardate = int(100 * (31.0 * random.random() + 20.0)) * 100

        self.initial_planets = random.randint(1, 10)
        self.initial_romulans = random.randint(2 * int(self.difficulty), 3 * int(self.difficulty))
        self.initial_timeAvail = 7 * int(self.gameLength)

        # compute number of klingons
        # .15 & .1 constants taken from Super Star Trek.  Also constants for % of commanders and resources
        # taken from same source
        # yields approximately gameLength * 14 *
        self.initial_klingons = int(
            self.initial_timeAvail * 2 * (
                0.15 + 0.1 * (int(self.difficulty) + random.randrange(-1, 1)) * int(self.difficulty)))
        assert self.initial_klingons > 0
        # only ever 1 (for now)
        self.initial_superCommanders = int(self.difficulty > GameDifficulty.Fair)
        # approximately 1 in 16, but at least 1
        self.initial_commanders = self.difficulty + random.randint(0, self.initial_klingons / 16)
        assert self.initial_commanders + self.initial_superCommanders <= self.initial_klingons

        # resources of the federation to withstand the onslaught
        self.initial_bases = random.randint(2, 5)
        self.initial_resources = (self.initial_klingons + 4 * self.initial_commanders) * self.initial_timeAvail

        if self.initial_klingons > 50:
            self.initial_bases += 1

        # set current values
        self.stardate = self.initial_stardate
        self.cur_romulans = self.initial_romulans
        self.cur_klingons = self.initial_klingons
        self.cur_commanders = self.initial_commanders
        self.cur_superCommanders = self.initial_superCommanders
        self.cur_planets = self.initial_planets
        self.cur_bases = self.initial_bases
        self.cur_resources = self.initial_resources
        self.galaxy = Galaxy()

        # build the galaxy with expected contents

    def BuildGalaxy(self):
        for r in self.galaxy.size:
            for c in self.galaxy.size:
                self.galaxy[Coordinate(r, c)] = Sector(r, c)

    def damageFactor(self, player):
        return 0.5 * int(self.difficulty) * player.handicap

    @staticmethod
    def processWarp(player, direction, factor):
        (delta, energy_cost) = calc_move_offsets(direction, factor)
        player.move(delta, energy_cost)

    def Move(self, player, bias):
        direction = None
        factor = None

        def setDir(val):
            nonlocal direction
            direction = val

        def setFactor(val):
            nonlocal factor
            factor = val
            self.processWarp(self.player, direction, factor / bias)

        UserInput.queue_query(
            [
                UserInput.NumQuery(minval=0, maxval=359, prompt='Direction (0-359 degrees, 0 = up)',
                                   onComplete=setDir),
                UserInput.NumQuery(minval=1, maxval=9, prompt='Warp Factor (1-9)',
                                   onComplete=setFactor)
            ])

    def Warp(self, player):
        self.Move(self.player, 1)

    def Impulse(self, player):
        self.Move(self.player, 10)

    def LongRangeScan(self, player):
        rows = Util.inclusive_range(player.galaxy_coord.row - 1, player.galaxy_coord.row + 1)
        cols = Util.inclusive_range(player.galaxy_coord.col - 1, player.galaxy_coord.col + 1)
        for row in rows:
            for col in cols:
                if Coordinate(row, col) in player.galaxy:
                    player.updateStarChart(self.galaxy[Coordinate(row, col)])

    @staticmethod
    def Dock(player):
        rows = range(player.sector_coord.row - 1, player.sector_coord.row + 2)
        cols = range(player.sector_coord.col - 1, player.sector_coord.col + 2)
        for row in rows:
            for col in cols:
                c = Coordinate(row, col)
                if c in player.sector and isinstance(player.sector[c], Base):
                    player.dock(player.sector[c])

    def process_command(self, cmd):
        cmd = cmd.upper()
        if cmd == 'W':
            self.Warp(self.player)
        elif cmd == 'I':
            self.Impulse(self.player)
        elif cmd == 'G':
            pass
            # Globals.g_galaxy.printGalaxy(self.player, False)
        elif cmd == 'L':
            self.LongRangeScan(self.player)
        elif cmd == 'D':
            self.Dock(self.player)
        #else:
        #    UserInput.setCurrentError('invalid cmd:', cmd)

    def draw_active_game_screen(self):
        galbbox = self.galaxy.print(self.player, 0, 0, range(0, Constants.GALAXY_SIZE), range(0, Constants.GALAXY_SIZE))
        rect = Drawing.print_at(0, galbbox.bottom + 5, 'Current Sector: {0}', self.player.galaxy_coord)
        sectorbox = self.galaxy[self.player.galaxy_coord].print_sector(0, rect.bottom + 1)
        self.player.display_status(sectorbox.right + 5, rect.bottom + 1, self)

        # display current input prompt, input text, and error message if any
        UserInput.drawInput(0, sectorbox.bottom + 5)

    def drawframe(self):
        self.draw_active_game_screen()
        # if no queries are pending, then queue the command prompt
        if not UserInput.has_query():
            UserInput.queue_query(
                [UserInput.ChoiceQuery(choices=['W', 'L', 'G', 'I'], prompt=_command_prompt, errMsg="Invalid Command!",
                                       onComplete=self.process_command)
                 ])
