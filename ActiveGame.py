""" One game pass, options, etc. """
import Drawing
from Galaxy import Galaxy
from Player import Player
from Coordinate import *
import UserInput
from Base import Base
import Globals
from IGameStage import IGameStage
import Util

_command_prompt = '(W)arp, (I)mpulse, (L)ong Range Scan'


class ActiveGame(IGameStage):
    def __init__(self):
        self.galaxy = Galaxy()
        self.player = Player(self.galaxy)
        self.game_over = False

    def Move(self, player, bias):

        direction = None
        factor = None
        def processWarp(player, direction, factor):
            (delta, energy_cost) = calc_move_offsets(direction, factor)
            player.move(delta, energy_cost)

        def setDir(val):
            nonlocal direction
            direction = val

        def setFactor(val):
            nonlocal factor
            factor = val
            processWarp(self.player, direction, factor/bias)

        UserInput.queue_query(
            [
                UserInput.NumQuery(minval=0, maxval=359, prompt='Direction (0-359 degrees, 0 = up)',
                                   onComplete=setDir),
                UserInput.NumQuery(minval=1, maxval=9, prompt='Warp Factor (1-9)',
                                   onComplete= setFactor)
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
                    player.galaxy[Coordinate(row, col)].unHide()


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
            Globals.g_galaxy.printGalaxy(self.player, False)
        elif cmd == 'L':
            self.LongRangeScan(self.player)
        elif cmd == 'D':
            self.Dock(self.player)
        else:
            UserInput.setCurrentError('invalid cmd:', cmd)

    def draw_active_game_screen(self):
        galbbox = self.galaxy.print(self.player, 0,0, range(0,Constants.GALAXY_SIZE), range(0,Constants.GALAXY_SIZE))
        rect = Drawing.print_at(0, galbbox.bottom + 5, 'Current Sector: {0}', self.player.galaxy_coord)
        sectorbox = self.galaxy[self.player.galaxy_coord].print_sector(0, rect.bottom + 1)
        self.player.display_status(sectorbox.right + 5, rect.bottom + 1)

        # display current input prompt, input text, and error message if any
        UserInput.drawInput(0, sectorbox.bottom + 5)

    def drawframe(self):
        self.draw_active_game_screen()
        # if no queries are pending, then queue the command prompt
        if not UserInput.has_query():
            UserInput.queue_query(
                [UserInput.ChoiceQuery(choices=['W', 'L', 'I'], prompt=_command_prompt, errMsg="Invalid Command!",
                                       onComplete=self.process_command)
                 ])
