#
# note this game uses tkinter, not pygame for output for a couple of simple reason
# First, it is meant to go with the book "Help Your Kids with Computer Coding", which
# uses tkinter.
# Second, while the game uses a graphics output mode, it's emulating old text based games, and uses
# graphics as a replacement for the curses library to be windows and cross-platform and
# this mode avoids the complexity of surface management.
# A future evolution of this will probably use pygame

import random

from ActiveGame import ActiveGame
from Coordinate import *
from UserInput import queue_input, command_input
import Globals
import time
import Drawing

def DisplayOpeningSequence():
    pass


def RunPreGameMenu():
    # Initialize a New ActiveGame
    return ActiveGame()


def InjectTestInput():
    # walk galaxy
    # queue_input(["w", "270", "2", "g"])
    # queue_input(["w", "90", "1", "L", "g", "w", "180", "3", "g", "l", "g" ])
    # queue_input(["w", "270", "3", "L", "w", "270", "3", "L", "w", "270", "3", "L", "g"])
    # queue_input(["w", "20", "3", "L", "g"])
    # queue_input(["w", "0", "3", "L", "g"])
    # queue_input(["w", "0", "3", "L", "g"])
    # queue_input(["w", "90", "3", "L", "g"])
    # queue_input(["w", "90", "3", "L", "g"])
    # queue_input(["w", "90", "1", "L", "g"])

    # dock at close base
    queue_input(["w", "180", "2", "i", "0", "6", "i", "90", "1"])

    # Globals.g_galaxy.unHideAll()


def z():
    DisplayOpeningSequence()

    # main loop
    Globals.exit_game = False

    while not Globals.g_exit_game:
        # collect game options, etc.
        game = RunPreGameMenu()

        # setup any tests
        InjectTestInput()

        # run one game (until ActiveGame Over)
        while not game.game_over:
            game.draw_current_sector()
            #            cmd = command_input()
            #            game.process_command(cmd)
            Globals.g_tk_root_window.update()
            time.sleep(0.01)

        # query play again
        Globals.g_exit_game = True


# main code
def main():
    # global Globals.g_galaxy
    # global Globals.g_player
    # initialize game.  Currently always using the same see for testing
    random.seed(1)
    Globals.g_game_mode = Constants.GameMode.WelcomeAnimation

    Drawing.InitializeGameWindow(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
    Globals.g_game_stage = ActiveGame()
    Globals.g_game_stage.run()
    Globals.g_tk_root_window.mainloop()


if __name__ == '__main__':
    main()
