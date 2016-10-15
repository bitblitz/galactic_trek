import math
import Constants


class Coordinate:
    def __init__(self, r=0, c=0):
        """ stores an integer row and column coordinate for a rectangular coordinate system.
            """
        self.row = r
        self.col = c

    def __repr__(self):
        return 'Coord({self.row}, {self.col})'.format(self=self)

    def __str__(self):
        return '({self.row}, {self.col})'.format(self=self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.row * other, self.col * other)
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.row + other.row, self.col + other.col)
        elif isinstance(other, (int, float)):
            return Coordinate(self.row + other, self.col + other)
        else:
            return NotImplemented

    def restrict_to_bounds(self, low, high):
        self.row = apply_bound(self.row, low.row, high.row)
        self.col = apply_bound(self.col, low.col, high.col)
        return self


# helper math functions
def apply_bound(val, low, high):
    if val < low:
        val = low
    elif val > high:
        val = high
    return val


def convert_direction(direction):
    # convert map direction (0 degrees = up, clockwise) to
    # trigonometric angle (0 = +x direction, 90 = up, counter-clockwise)
    # requires input direction is in [0-360]
    # returns radians
    assert 0 <= direction <= 360, "invalid direction conversion"

    theta = 90 - direction
    if theta < 0:
        theta += 360

    return math.radians(theta)


def abs_ceil(x):
    # truncate value towards 
    if x < 0:
        x = math.floor(x)
    else:
        x = math.ceil(x)
    return x


def calc_energy_cost(warp_factor):
    if warp_factor >= 1:
        return int(Constants.WARP_COST * warp_factor * warp_factor)  # warp engines
    return int(Constants.WARP_COST * warp_factor)  # impulse engines


def calc_move_offsets(direction, warp_factor):
    # while the user perceives the galaxy as Constants.GALAXY_SIZE sectors of Constants.SECTOR_SIZE, logically the
    # galaxy is a flat grid of Constants.GALAXY_SIZE * Constants.SECTOR_SIZE coordinates across, so we calculate moves
    # in global coordinates.
    # one warp_factor is equivalent to exactly one Constants.SECTOR_SIZE of global coordinates.
    theta = convert_direction(direction)
    x = math.trunc(warp_factor * Constants.SECTOR_SIZE * math.cos(theta))
    y = -math.trunc(warp_factor * Constants.SECTOR_SIZE * math.sin(theta))

    return Coordinate(y, x), calc_energy_cost(warp_factor)


def galsec_to_global(gal: Coordinate, sec: Coordinate) -> Coordinate:
    # convert galactic/sector coord pair to global coordinate
    return (gal * Constants.SECTOR_SIZE) + sec


def global_to_galsec(global_coord: Coordinate) -> (Coordinate, Coordinate):
    # convert galactic/sector coord pair to global coordinate
    gal = Coordinate(int(global_coord.row / Constants.SECTOR_SIZE), int(global_coord.col / Constants.SECTOR_SIZE))
    sec = global_coord + (gal * -Constants.SECTOR_SIZE)
    return gal, sec


def calc_global_move(delta, gal_coord: Coordinate, sector_coord: Coordinate) -> Coordinate:
    gl = galsec_to_global(gal_coord, sector_coord)

    # debug_print('global1:', gl)
    # debug_print('delta:', delta)

    gl += delta
    gl.restrict_to_bounds(Coordinate(0, 0), Coordinate(Constants.GALAXY_SIZE * Constants.SECTOR_SIZE - 1,
                                                       Constants.GALAXY_SIZE * Constants.SECTOR_SIZE - 1))
    # debug_print('global2:', gl)
    # debug_print('global2gs:',  global_to_galsec(gl))

    return global_to_galsec(gl)


# noinspection PyAugmentAssignment
def tests():
    print('running tests')
    # check some basic coordinate conversions
    gal = Coordinate(1, 2)
    sec = Coordinate(3, 4)
    gl = galsec_to_global(gal, sec)
    assert gl.row == gal.row * Constants.SECTOR_SIZE + sec.row
    assert gl.col == gal.col * Constants.SECTOR_SIZE + sec.col
    g2, s2 = global_to_galsec(gl)
    assert gal == g2
    assert sec == s2
    gal = gal * 3
    assert gal.row == 3 and gal.col == 6
    sec += Coordinate(-1, -3)
    assert sec.row == 2 and sec.col == 1


if __name__ == '__main__':
    tests()
