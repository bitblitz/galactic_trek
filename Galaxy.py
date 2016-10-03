import Constants
from Coordinate import Coordinate
from Sector import Sector


class Galaxy(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = range(Constants.GALAXY_SIZE)
        for r in self.size:
            for c in self.size:
                self[Coordinate(r, c)] = Sector(r, c)

    def printRowSep(self, player, row, cols):
        playerIsRightCol = (player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        playerIsThisRow = (row == player.galaxy_coord.row)
        playerIsPrevRow = (row == player.galaxy_coord.row + 1)
        for c in cols:
            if c not in self.size:
                continue

            if c == player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                print('************', end='')
            elif c - 1 == player.galaxy_coord.col and (playerIsThisRow or playerIsPrevRow):
                print('*-----------', end='')
            else:
                print('------------', end='')

        # fill in the last character of the row divider
        if (playerIsThisRow or playerIsPrevRow) and playerIsRightCol:
            print('*')
        else:
            print('-')

    def printGalaxy(self, player, showHidden):
        self.print(player, self.size, self.size, showHidden)

    def unHideAll(self):
        for r in range(Constants.GALAXY_SIZE):
            for c in range(Constants.GALAXY_SIZE):
                self[Coordinate(r, c)].unHide()

    # noinspection PyPep8,PyPep8
    def print(self, player, rows: range, cols: range, showHidden):
        playerIsRightCol = (player.galaxy_coord.col == Constants.GALAXY_SIZE - 1)
        for r in rows:
            if r not in self.size:
                continue

            playerIsThisRow = (r == player.galaxy_coord.row)

            # draw top border
            self.printRowSep(player, r, cols)

            # print top data row for sector
            for c in cols:
                if Coordinate(r, c) not in self:
                    continue

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    print('* ', end='')
                else:
                    print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    print('s:', len(s.stars), 'e:', len(s.enemies), sep=' ', end=' ')
                else:
                    print('  ', ' ', '  ', ' ', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                print('*', end='')
            else:
                print('|', end='')

            print('')
            # print second row
            for c in cols:
                if Coordinate(r, c) not in self:
                    continue

                if playerIsThisRow and (
                                c == player.galaxy_coord.col or c - 1 == player.galaxy_coord.col):
                    print('* ', end='')
                else:
                    print('| ', end='')

                s = self[Coordinate(r, c)]
                if showHidden or not s.hidden:
                    print('b:', len(s.bases), 'p:', len(s.planets), sep=' ', end=' ')
                else:
                    print('  ', ' ', '  ', ' ', sep=' ', end=' ')

            # print right hand cell separator
            if playerIsThisRow and playerIsRightCol:
                print('*', end='')
            else:
                print('|', end='')

            print('')

        # draw bottom
        self.printRowSep(player, Constants.GALAXY_SIZE, cols)
