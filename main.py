import pygame

from engine.Engine import Engine

pygame.init()
pygame.font.init()

# TODO create config
# -------editables-------
FPS = 30
MAP_SIZE = 15      # in tiles
WINDOW_SIZE = (MAP_SIZE * 33 + 400 , MAP_SIZE * 33 + 300)
PATH_TO_MAP = "resources/map_layouts/layout2.txt"
# -----------------------

# screen handle
hScreen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption('Czerwony ciągnik')

fpsClock = pygame.time.Clock()

# create and init game engine
engine = Engine(MAP_SIZE, PATH_TO_MAP)

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
