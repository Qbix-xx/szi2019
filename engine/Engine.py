import sys

import pygame
from pygame.locals import *

from entities.Ground.Grass import Grass
from entities.Ground.Road import Road
from entities.Tractor import Tractor


class Engine():
    def __init__(self, map_size, path_to_map_layout):

        self._MAP_SIZE = map_size

        # set fonts for rendering text
        self.__set_fonts_and_colours()
        self.__load_map_from_file(path_to_map_layout)
        self.__init_sprites()
        self.__init_tractor()

        # create game map from layout
        self.__game_map_init()

        # 0 = menu, 1 = playing, ...(?)
        # self.gameState = 0 # TODO: idk, haven't found purpose for this yet

    def __init_sprites(self):
        self._ground_sprite_group = pygame.sprite.Group()
        self._tractor_sprite_group = pygame.sprite.Group()

    def __init_tractor(self):
        self.tractor = Tractor(self._MAP_SIZE)
        self._tractor_sprite_group.add(self.tractor)

    def __set_fonts_and_colours(self):
        self._ground_name_font = pygame.font.SysFont('Helvetica', 30)
        self._ground_name_colour = (0, 0, 0)
        self._ground_stats_font = pygame.font.SysFont('Helvetica', 20)
        self._ground_stats_colour = (0, 0, 0)

        self._tractor_name_font = pygame.font.SysFont('Helvetica', 30)
        self._tractor_name_colour = (0, 0, 0)
        self._tractor_stats_font = pygame.font.SysFont('Helvetica', 20)
        self._tractor_stats_colour = (0, 0, 0)

    def __load_map_from_file(self, path):
        with open(path) as textfile:
            self._mapLayoutFile = list(line.split(" ") for line in textfile)

    def __game_map_init(self):
        # list of lists (2d grid) containing all the objects on the map
        # mwiecek: init empty game map matrix
        self._game_map = [[None] * self._MAP_SIZE for _ in range(self._MAP_SIZE)]

        for i in range(self._MAP_SIZE):
            for j in range(self._MAP_SIZE):
                if self._mapLayoutFile[i][j] == "1":
                    self._game_map[i][j] = Road(i * 32 + i + 32, j * 32 + j + 32)
                elif self._mapLayoutFile[i][j] == "2":
                    self.tractor.set_rect(i, j)
                else:
                    self._game_map[i][j] = Grass(i * 32 + i + 32, j * 32 + j + 32)

        self._ground_sprite_group.add(self._game_map)

    def render(self, hScreen):
        # grey background
        hScreen.fill([100, 100, 100])

        # black background below map grid to make lines more visible
        pygame.draw.rect(hScreen, [0, 0, 0], (32, 32, 33 * self._MAP_SIZE, 33 * self._MAP_SIZE))

        self.__render_ground_stats(hScreen)
        self.__render_tractor_storage_stats(hScreen)
        # old way of map rendering
        # for i in range(self._MAP_SIZE):
        #     for j in range(self._MAP_SIZE):
        # hScreen.blit(self._game_map[i][j].get_surface_image(), (self._game_map[i][j].rect.x, self._game_map[i][j].rect.y))

        # if pygame.sprite.collide_rect(self.tractor, self._game_map[i][j]):
        # name_surface = self.ground_name_font.render(self._game_map[i][j].name, True, (0, 0, 0))
        # hScreen.blit(name_surface, (self._MAP_SIZE * 32 + 150, 80))

        # m = 0
        # for k, l in self._game_map[i][j].get_stats().items():
        #     stats_surface = self.ground_stats_font.render(str(k) + ": " + str(l), True, (0, 0, 0))
        #     hScreen.blit(stats_surface, (self._MAP_SIZE * 32 + 150, 130 + m * 30))
        #     m += 1

        self._ground_sprite_group.draw(hScreen)
        self._tractor_sprite_group.draw(hScreen)

    def __render_name_surface(self, font, colour, string_name, position_x, position_y, hScreen):
        name_surface = font.render(
            string_name,
            True,
            colour
        )
        hScreen.blit(name_surface, (position_x * 33, position_y * 33))

    def __render_stats_surface(self, dict, font, colour, position_x, position_y, hScreen):
        iterator_over_stat_dict_key = 0
        for stat_name, stat_level in dict:
            stats_surface = font.render(
                str(stat_name) + ": " + str(stat_level) + "%",
                True,
                colour
            )

            hScreen.blit(stats_surface, (position_x * 33, position_y * 33 + iterator_over_stat_dict_key * 33))
            iterator_over_stat_dict_key += 1

    def __render_tractor_storage_stats(self, hScreen):
        self.__render_name_surface(
            self._tractor_name_font,
            self._tractor_name_colour,
            "Tractor Storage",
            1, self._MAP_SIZE + 2,
            hScreen
        )

        self.__render_stats_surface(
            self.tractor.storage_stats.items(),
            self._tractor_stats_font,
            self._tractor_stats_colour,
            1, self._MAP_SIZE + 3,
            hScreen
        )

    def __render_ground_stats(self, hScreen):
        self.__render_name_surface(
            self._ground_name_font,
            self._ground_name_colour,
            self._game_map[self.tractor.index_x][self.tractor.index_y].name,
            self._MAP_SIZE + 4, 1,
            hScreen
        )

        self.__render_stats_surface(
            self._game_map[self.tractor.index_x][self.tractor.index_y].get_ground_stats().items(),
            self._ground_stats_font,
            self._ground_stats_colour,
            self._MAP_SIZE + 4, 2,
            hScreen
        )

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.tractor.move_right()
                elif event.key == K_LEFT:
                    self.tractor.move_left()
                elif event.key == K_DOWN:
                    self.tractor.move_down()
                elif event.key == K_UP:
                    self.tractor.move_up()
                elif event.key == K_f:
                    self.do_things()

    def update_sprites(self):
        self._tractor_sprite_group.update()

    def do_things(self):
        if self.tractor.operation("irrigation"):
            self._game_map[self.tractor.index_x][self.tractor.index_y].irrigate(self.tractor.get_irrigate_rate())
        if self.tractor.operation("fertilizer"):
            self._game_map[self.tractor.index_x][self.tractor.index_y].fertilize(self.tractor.get_fertilize_rate())
