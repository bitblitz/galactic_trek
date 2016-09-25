import Constants
from Coordinate import Coordinate
from Sector import Sector
import Globals


class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)
        for r in self.size:
            for c in self.size:
                self[Coordinate(r, c)] = Sector(r, c)

    def printRowSep(self, r):
        playerIsRightCol = (Globals.g_player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        playerIsThisRow = (r == Globals.g_player.galaxy_coord.row)
        playerIsPrevRow = (r == Globals.g_player.galaxy_coord.row + 1)
        for c in self.size:
            if c == Globals.g_player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                print('************', end='')
            elif c - 1 == Globals.g_player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
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
        playerIsRightCol = (Globals.g_player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        # playerIsPrevRow = (Globals.g_player.galaxy_coord.row == Constants.GALAXY_SIZE - 1)
        # playerIsThisRow = False
        # playerIsPrevRow = False
        for r in self.size:
            playerIsThisRow = (r == Globals.g_player.galaxy_coord.row)
            # playerIsPrevRow = (r == Globals.g_player.galaxy_coord.row + 1)

            # draw top border
            self.printRowSep(r)

            # print top data row for sector
            for c in self.size:
                if playerIsThisRow and (
                        c == Globals.g_player.galaxy_coord.col or c - 1 == Globals.g_player.galaxy_coord.col):
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
                if playerIsThisRow and (
                        c == Globals.g_player.galaxy_coord.col or c - 1 == Globals.g_player.galaxy_coord.col):
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
