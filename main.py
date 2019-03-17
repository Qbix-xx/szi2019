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

# screen handle
hScreen = pygame.display.set_mode(WINDOW_SIZE)

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
