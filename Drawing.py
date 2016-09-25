import Globals


def draw_current_sector():
    print('Current Sector: ', Globals.g_player.galaxy_coord)
    Globals.g_galaxy[Globals.g_player.galaxy_coord].print_sector()
    Globals.g_player.display()
