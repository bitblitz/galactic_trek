import Constants
from Coordinate import Coordinate
from Sector import Sector
import Drawing


class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)

    def printRowSep(self, player, lineator, row, cols):
        playerIsRightCol = (player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        playerIsThisRow = (row == player.galaxy_coord.row)
        playerIsPrevRow = (row == player.galaxy_coord.row + 1)
        for c in cols:
            if c not in self.size:
                continue

            if c == player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                lineator.print('************', end='')
            elif c - 1 == player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                lineator.print('*-----------', end='')
            else:
                lineator.print('------------', end='')

        # fill in the last character of the row divider
        if (playerIsThisRow or playerIsPrevRow) and playerIsRightCol:
            lineator.print('*')
        else:
            lineator.print('-')

    # def printGalaxy(self, player, showHidden):
    #    self.print(player, self.size, self.size, showHidden)

    def unHideAll(self):
        for r in range(Constants.GALAXY_SIZE):
            for c in range(Constants.GALAXY_SIZE):
                self[Coordinate(r, c)].unHide()

    # noinspection PyPep8,PyPep8
    def print(self, player, left, top, rows: range, cols: range, showHidden=False):
        lineator = Drawing.Lineator(left, top)
        playerIsRightCol = (player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        for r in rows:
            if r not in self.size:
                continue

            playerIsThisRow = (r == player.galaxy_coord.row)

            # draw top border
            self.printRowSep(player, lineator, r, cols)

            # print top data row for sector
            for c in cols:
                if Coordinate(r, c) not in self:
                    continue

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    lineator.print('* ', end='')
                else:
                    lineator.print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    lineator.print('s:', len(s.stars), 'e:', len(s.enemies), sep=' ', end=' ')
                else:
                    lineator.print('  ', ' ', '  ', ' ', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                lineator.print('*', end='')
            else:
                lineator.print('|', end='')

            lineator.print('')
            # print second row
            for c in cols:
                if Coordinate(r, c) not in self:
                    continue

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    lineator.print('* ', end='')
                else:
                    lineator.print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    lineator.print('b:', len(s.bases), 'p:', len(s.planets), sep=' ', end=' ')
                else:
                    lineator.print('  ', ' ', '  ', ' ', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                lineator.print('*', end='')
            else:
                lineator.print('|', end='')

            lineator.print('')

        # draw bottom
        self.printRowSep(player, lineator, Constants.GALAXY_SIZE, cols)
        return lineator.bbox
