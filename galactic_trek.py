import random

from Drawing import draw_current_sector
from Galaxy import Galaxy
from Player import Player
from Coordinate import *
from UserInput import num_input, queue_input, command_input
import Globals


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

def LongRangeScan(player):
    rows = range(player.galaxy_coord.row-1, player.galaxy_coord.row+2)
    cols = range(player.galaxy_coord.col-1, player.galaxy_coord.col+2)
    for row in rows:
        for col in cols:
            if Coordinate(row,col) in player.galaxy:
                player.galaxy[Coordinate(row,col)].unHide()

    player.galaxy.print(Globals.g_player, rows, cols, False)

def process_command(cmd):
    cmd = cmd.upper()
    if cmd == 'W':
        Warp(Globals.g_player)
    elif cmd == 'I':
        Impulse(Globals.g_player)
    elif cmd == 'G':
        Globals.g_galaxy.printGalaxy(Globals.g_player, False)
    elif cmd == 'L':
        LongRangeScan(Globals.g_player)
    else:
        print('invalid cmd:', cmd)


# main code
def main():
    # global Globals.g_galaxy
    # global Globals.g_player
    # initialize game
    random.seed(1)
    Globals.g_galaxy = Galaxy()
    Globals.g_player = Player(Globals.g_galaxy)
    Globals.g_galaxy.printGalaxy(Globals.g_player, False)
    #queue_input(["w", "270", "2", "g"])
    queue_input(["w", "90", "1", "L", "g"])

    # main loop
    while True:
        draw_current_sector()
        cmd = command_input()
        process_command(cmd)


if __name__ == '__main__':
    main()
