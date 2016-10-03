""" One game pass, options, etc. """
import Drawing
from Galaxy import Galaxy
from Player import Player
from Coordinate import *
from UserInput import num_input
from Base import Base
import Globals
from IGameStage import IGameStage


class ActiveGame(IGameStage):
    def __init__(self):
        self.galaxy = Galaxy()
        self.player = Player(self.galaxy)
        self.game_over = False

    @staticmethod
    def Warp(player):
        direction = num_input('Warp Direction (0-359 degrees, 0 = up)', 0, 360)
        factor = num_input('Warp Factor (1-9)', 1, 9)

        (delta, energy_cost) = calc_move_offsets(direction, factor)
        player.move(delta, energy_cost)

    @staticmethod
    def Impulse(player):
        direction = num_input('Warp Direction (0-359 degrees, 0 = up)', 0, 360)
        factor = num_input('Impulse Factor (1-9)', 1, 9)

        (delta, energy_cost) = calc_move_offsets(direction, factor / 10)
        player.move(delta, energy_cost)

    def LongRangeScan(self, player):
        rows = range(player.galaxy_coord.row - 1, player.galaxy_coord.row + 2)
        cols = range(player.galaxy_coord.col - 1, player.galaxy_coord.col + 2)
        for row in rows:
            for col in cols:
                if Coordinate(row, col) in player.galaxy:
                    player.galaxy[Coordinate(row, col)].unHide()

        player.galaxy.print(self.player, rows, cols, False)

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
            print('invalid cmd:', cmd)

    def draw_current_sector(self):
        Drawing.draw_current_sector(self)

    def animate(self):
        self.draw_current_sector()
