from enum import Enum

GALAXY_SIZE = 10
SECTOR_SIZE = 10
WARP_COST = 100  # cost for warp 1.
# negative planets are just used to skew the distribution
# and make it less probable there is a planet in any given sector
MIN_PLANETS = -20
MAX_PLANETS = 10
MIN_STARS = 0
MAX_STARS = 6
PROB_BASE = 10  # out of 100
MIN_ENEMY = -5
MAX_ENEMY = 8
MIN_ENEMY_ENERGY = 800
MAX_ENEMY_ENERGY = 1500
PLAYER_INITIAL_ENERGY = 10000
PLAYER_INITIAL_TORPS = 5
PLAYER_MAX_TORPS = 10
PLAYER_INITIAL_SHIELD = 2000
BASE_INITIAL_ENERGY = 100000
BASE_INITIAL_TORPS = 100
BASE_INITIAL_SHIELD = 10000
# Easy start means the first sector will have no enemies
EASY_START = True
YELLOW_ALERT_ENERGY = 2000  # less than this is yellow alert
# sound Ids
ERROR_SOUND = 1
ALERT_SOUND = 2

APPLICATION_TITLE = "Galactic Trek"

# TKinter related constants
DEFAULT_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = "Courier"
DEFAULT_FONT_SIZE = 10
BIG_FONT_SIZE = 12
SMALL_FONT_SIZE = 9
CODEBOX_FONT_SIZE = 9
TEXTBOX_FONT_SIZE = DEFAULT_FONT_SIZE

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000


class GameMode(Enum):
    WelcomeAnimation = 1
    MainMenu = 2
    Playing = 3
    GameOver = 4
    Exiting = 5
