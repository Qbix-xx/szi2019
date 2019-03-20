import sys

import pygame
from pygame.locals import *

from entities.Ground.AbstractHarvestable import AbstractHarvestable
from entities.Ground.Grass import Grass
from entities.Ground.Plant import Plant
from entities.Ground.Road import Road
from entities.Tractor import Tractor


class Engine:
    def __init__(self, map_size, path_to_map_layout):

        self.__MAP_SIZE = map_size
        self.__start_time = pygame.time.get_ticks()

        # set fonts for rendering text
        self.__set_fonts_and_colours()
        self.__load_map_from_file(path_to_map_layout)
        self.__init_sprites_group()
        self.__init_tractor()

        # create game map from layout
        self.__game_map_init()

        # 0 = menu, 1 = playing, ...(?)
        # self.gameState = 0 # TODO: idk, haven't found purpose for this yet

    def __init_sprites_group(self):
        self.__ground_sprite_group = pygame.sprite.Group()
        self.__tractor_sprite_group = pygame.sprite.Group()

    def __init_tractor(self):
        self.__tractor = Tractor(self.__MAP_SIZE)
        self.__tractor_sprite_group.add(self.__tractor)

    def __set_fonts_and_colours(self):
        self.__ground_name_font = pygame.font.SysFont('Helvetica', 30)
        self.__ground_name_colour = (0, 0, 0)
        self.__ground_stats_font = pygame.font.SysFont('Helvetica', 20)
        self.__ground_stats_colour = (0, 0, 0)

        self.__tractor_name_font = pygame.font.SysFont('Helvetica', 30)
        self.__tractor_name_colour = (0, 0, 0)
        self.__tractor_stats_font = pygame.font.SysFont('Helvetica', 20)
        self.__tractor_stats_colour = (0, 0, 0)

    def __load_map_from_file(self, path):
        with open(path) as textfile:
            self.__mapLayoutFile = list(line.split(" ") for line in textfile)

    def __game_map_init(self):
        # list of lists (2d grid) containing all the objects on the map
        # mwiecek: init empty game map matrix
        self.__game_map = [[[]] * self.__MAP_SIZE for _ in range(self.__MAP_SIZE)]

        for i in range(self.__MAP_SIZE):
            for j in range(self.__MAP_SIZE):

                self.__game_map[i][j] = []

                if self.__mapLayoutFile[i][j] == "1":
                    self.__game_map[i][j].append(Road(i * 32 + i + 32, j * 32 + j + 32))
                elif self.__mapLayoutFile[i][j] == "2":
                    self.__tractor.set_rect(i, j)
                elif self.__mapLayoutFile[i][j] == "3":
                    self.__game_map[i][j].append(Grass(i * 32 + i + 32, j * 32 + j + 32))
                    self.__game_map[i][j].append(Plant(i * 32 + i + 32, j * 32 + j + 32))
                else:
                    self.__game_map[i][j].append(Grass(i * 32 + i + 32, j * 32 + j + 32))

        self.__ground_sprite_group.add(self.__game_map)

    def render(self, hScreen):
        # grey background
        hScreen.fill([100, 100, 100])

        # black background below map grid to make lines more visible
        pygame.draw.rect(hScreen, [0, 0, 0], (32, 32, 33 * self.__MAP_SIZE, 33 * self.__MAP_SIZE))

        self.__render_ground_stats(hScreen)
        self.__render_tractor_storage_stats(hScreen)

        # for ground in self.__ground_sprite_group:
        #
        # for object_in in ground.image_list:
        #     ground.draw_warinig()
        #     image_list[object_in]

        # TODO refractor it later
        self.__ground_sprite_group.draw(hScreen)
        self.__tractor_sprite_group.draw(hScreen)

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
            self.__tractor_name_font,
            self.__tractor_name_colour,
            "Tractor Storage",
            1, self.__MAP_SIZE + 2,
            hScreen
        )

        self.__render_stats_surface(
            self.__tractor.storage_stats.items(),
            self.__tractor_stats_font,
            self.__tractor_stats_colour,
            1, self.__MAP_SIZE + 3,
            hScreen
        )

    def __render_ground_stats(self, hScreen):

        local_field_list = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
        self.__render_name_surface(
            self.__ground_name_font,
            self.__ground_name_colour,
            local_field_list[len(local_field_list) - 1].get_name(),
            self.__MAP_SIZE + 4, 1,
            hScreen
        )

        if isinstance(local_field_list[len(local_field_list) - 1],
                      AbstractHarvestable):
            self.__render_stats_surface(
                local_field_list[len(local_field_list) - 1].get_ground_stats().items(),
                self.__ground_stats_font,
                self.__ground_stats_colour,
                self.__MAP_SIZE + 4, 2,
                hScreen
            )

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.__tractor.move_right()
                elif event.key == K_LEFT:
                    self.__tractor.move_left()
                elif event.key == K_DOWN:
                    self.__tractor.move_down()
                elif event.key == K_UP:
                    self.__tractor.move_up()
                elif event.key == K_f:
                    self.do_things()

    def update_sprites(self):
        self.__tractor_sprite_group.update()
        self.__ground_sprite_group.update()

        if (pygame.time.get_ticks() - self.__start_time) / 1000 > 4:
            self.__start_time = pygame.time.get_ticks()

            for ground_field in self.__ground_sprite_group:
                if isinstance(ground_field, AbstractHarvestable):
                    ground_field.grow()

    def do_things(self):
        local_field_instance = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
        if isinstance(local_field_instance[len(local_field_instance) - 1], AbstractHarvestable):
            if self.__tractor.operation("irrigation"):
                local_field_instance[len(local_field_instance) - 1] \
                    .irrigate(self.__tractor.get_irrigate_rate())
            if self.__tractor.operation("fertilizer"):
                local_field_instance[len(local_field_instance) - 1] \
                    .fertilize(self.__tractor.get_fertilize_rate())
