import Sector
import Constants
from Coordinate import Coordinate
import Drawing

class ChartSector:
    def __init__(self, sector: Sector.Sector):
        self.coordinate = sector.coordinate
        self.planets = len(sector.planets)
        self.bases = len(sector.bases)
        self.klingons = len(sector.klingons)
        self.stars = len(sector.stars)


# StarChart represents what a particular chart knows about the galaxy, which is always a subset of the details
# in the galaxy
class StarChart(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)

    def updateFromSector(self, sector: Sector):
        self[sector.coordinate] = ChartSector(sector)

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

    # noinspection PyPep8,PyPep8
    def print(self, player, left, top, rows: range, cols: range):
        lineator = Drawing.Lineator(left, top)
        playerIsRightCol = (player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        isHidden=True
        for r in rows:
            if r not in self.size:
                continue

            playerIsThisRow = (r == player.galaxy_coord.row)

            # draw top border
            self.printRowSep(player, lineator, r, cols)

            # print top data row for sector
            for c in cols:
                isHidden= Coordinate(r, c) not in self

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    lineator.print('* ', end='')
                else:
                    lineator.print('| ', end='')

                if not isHidden:
                    s = self[Coordinate(r, c)]
                    lineator.print('s:', s.stars, 'k:', s.klingons, sep=' ', end=' ')
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
                isHidden= Coordinate(r, c) not in self

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    lineator.print('* ', end='')
                else:
                    lineator.print('| ', end='')

                if not isHidden:
                    s = self[Coordinate(r, c)]
                    lineator.print('b:', s.bases, 'p:', s.planets, sep=' ', end=' ')
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
