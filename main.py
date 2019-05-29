import _thread as threading
import time

import pygame

from engine.Engine import Engine
from engine.GUI import GUI

pygame.init()
pygame.font.init()

# -------editables-------
FPS = 30
# MAP = "layout3_dev.txt"
DEFAULT_MAP_SIZE = 15      # in tiles
WINDOW_SIZE = (DEFAULT_MAP_SIZE * 33 + 450, DEFAULT_MAP_SIZE * 33 + 300)
# -----------------------

# screen handle
engine = Engine(WINDOW_SIZE)
# engine = Engine(MAP, WINDOW_SIZE)
# hScreen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption('Czerwony ciągnik')

fpsClock = pygame.time.Clock()

# create and init game engine
# engine.set_hScreen(hScreen)

# plants_update_thread = threading.start_new_thread(self.__update_plants, (0, 0))
# render_thread = threading.start_new_thread(render, (0, 0))
# todo add update thread asap

while True:
    # handle keyboard input
    engine.handle_keyboard()

    # update sprites
    engine.update()

    # render game
    engine.render()

    # draw everything from buffer on screen
    pygame.display.flip()
    fpsClock.tick(FPS)
