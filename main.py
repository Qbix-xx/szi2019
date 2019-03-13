import pygame as pg
import sys
from pygame.locals import *

pg.init()

# -------editables-------
FPS = 30
MAP_SIZE = 15      # in tiles
WINDOW_SIZE = (MAP_SIZE*33 + 500, MAP_SIZE*33 + 200)
# -----------------------

# 0 = menu, 1 = playing, ...(?)
gameState = 0

# list of lists (2d grid) containing all the objects on the map
Map = [[None] * MAP_SIZE for _ in range(MAP_SIZE)]


# loading map road layout from text file with "x y" values in each line for each road tile
mapLayoutFile = open("map_layouts/layout_15x15.txt", "r")

# !!!!!!!!!! ( to be reworked, map needs to hold objects instead of numbers) !!!!!!!!!!!!
for line in mapLayoutFile:
    x, y = map(int, line.strip().split())
    Map[x][y] = 1 # some pycharm warning here, not sure why


# screen handle
hScreen = pg.display.set_mode(WINDOW_SIZE)
# grey background
hScreen.fill([100, 100, 100])
pg.display.set_caption('Czarny ciągnik')

# placeholder sprites (to be replaced/removed)
grass = pg.image.load("sprites/grass.png")
dirt = pg.image.load("sprites/dirt.png")

# background below map grid just to make lines more visible (black)
pg.draw.rect(hScreen, [0, 0, 0], (28, 28, 33 * MAP_SIZE + 3, 33 * MAP_SIZE + 3))
fpsClock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        # elif event.type == KEYUP:
        # update and draw sprites/images/whatnot in the buffer
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                if Map[i][j] is None:
                    hScreen.blit(grass, (i * 32 + i + 30, j * 32 + j + 30))
                else:
                    hScreen.blit(dirt,  (i * 32 + i + 30, j * 32 + j + 30))

    # draw everything from buffer on screen
    pg.display.flip()
    fpsClock.tick(FPS)
