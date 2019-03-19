import pygame

from engine.Engine import Engine

pygame.init()
pygame.font.init()

# -------editables-------
FPS = 30
MAP_SIZE = 15      # in tiles
WINDOW_SIZE = (MAP_SIZE + 1024, MAP_SIZE + 1024)
PATH_TO_MAP = "resources/map_layouts/layout1.txt"
# WINDOW_SIZE = (MAP_SIZE*32+ 100, MAP_SIZE*32)
# -----------------------

<<<<<<< HEAD
# 0 = menu, 1 = playing, ...(?)
gameState = 0

# list of lists (2d grid) containing all the objects on the map
Map = [[None] * MAP_SIZE for _ in range(MAP_SIZE)]


# loading map road layout from text file with "x y" values in each line for each road tile
mapLayoutFile = open("map_layouts/layout_15x15.txt", "r")

# !!!!!!!!!! ( to be reworked, map needs to hold objects instead of numbers) !!!!!!!!!!!!
for line in mapLayoutFile:
    x, y = map(int, line.strip().split())
    Map[x][y] = 1  # some pycharm warning here, not sure why
=======
# screen handle
hScreen = pygame.display.set_mode(WINDOW_SIZE)
>>>>>>> 5016d1c41d0a5edcb78faffe914229579c467828

pygame.display.set_caption('Czarny ciągnik')

fpsClock = pygame.time.Clock()

# create and init game engine
engine = Engine(MAP_SIZE, PATH_TO_MAP)

# load maplayout to engine
# engine.load_map_from_file()

while True:
    # handle keyboard input
    engine.handle_keyboard()

    # update sprites
    engine.update_sprites()
    # render game
    engine.render(hScreen)

    # draw everything from buffer on screen
    pygame.display.flip()
    fpsClock.tick(FPS)
