import sys

import pygame
from pygame.locals import *

from entities.Barn import Barn
from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from entities.Ground.Grass import Grass
from entities.Ground.Plant import Plant
from entities.Ground.Road import Road
from entities.Ground.Tree import Tree
from entities.Tractor import Tractor
from entities.WaterContainer import WaterContainer


class Engine:
    def __init__(self, map_size, path_to_map_layout):

        self.__MAP_SIZE = map_size
        self.__start_time = pygame.time.get_ticks()

        # set fonts for rendering text
        self.__set_fonts_and_colours()

        self.__init_sprites()
        self.__init_map(path_to_map_layout)

        # plants delivered in total
        self.__plant_score = 0

    def __init_sprites(self):
        self.__init_sprites_group()
        self.__init_tractor()

    def __init_sprites_group(self):
        self.__ground_sprite_group = pygame.sprite.Group()
        self.__tractor_sprite_group = pygame.sprite.Group()
        self.__plants_sprite_group = pygame.sprite.Group()
        self.__solid_sprite_group = pygame.sprite.Group()

    def __init_tractor(self):
        self.__tractor = Tractor(self.__MAP_SIZE)
        self.__tractor_sprite_group.add(self.__tractor)

    def __init_map(self, path_to_map_layout):
        self.__load_map_from_file(path_to_map_layout)

        # create game map from layout
        self.__game_map_init()

    def __set_fonts_and_colours(self):
        self.__ground_text_header_font = pygame.font.SysFont('Helvetica', 30)
        self.__ground_text_header_colour = (0, 0, 0)
        self.__ground_stats_font = pygame.font.SysFont('Helvetica', 20)
        self.__ground_stats_colour = (0, 0, 0)

        self.__tractor_text_header_font = pygame.font.SysFont('Helvetica', 30)
        self.__tractor_text_header_colour = (0, 0, 0)
        self.__tractor_stats_font = pygame.font.SysFont('Helvetica', 20)
        self.__tractor_stats_colour = (0, 0, 0)

        self.__inventory_text_header_font = pygame.font.SysFont('Helvetica', 30)
        self.__inventory_text_header_colour = (0, 0, 0)
        self.__inventory_title_font = pygame.font.SysFont('Helvetica', 20)
        self.__inventory_title_colour = (0, 0, 0)

        # TODO move it to dict
        ground_fonts_colours = {
            "name_font": pygame.font.SysFont('Helvetica', 30),
            "name_colour": (0, 0, 0),
            "stats_font": pygame.font.SysFont('Helvetica', 20),
            "stats_colour": (0, 0, 0)
        }

        tractor_fonts_colours = {
            "name_font": pygame.font.SysFont('Helvetica', 30),
            "name_colour": (0, 0, 0),
            "stats_font": pygame.font.SysFont('Helvetica', 20),
            "stats_colour": (0, 0, 0)
        }

        self.__fonts_colours = {
            "ground": ground_fonts_colours,
            "tractor": tractor_fonts_colours
        }

    def __load_map_from_file(self, path):
        with open(path) as textfile:
            self.__mapLayoutFile = list(line.replace('\n', '').split(" ") for line in textfile)

    def __game_map_init(self):
        # list of lists (2d grid) containing all the objects on the map
        # mwiecek: init empty game map matrix
        self.__game_map = [[[]] * self.__MAP_SIZE for _ in range(self.__MAP_SIZE)]

        self.__create_map_from_layout()

        self.__ground_sprite_group.add(self.__game_map)

    def __create_solid_object(self, i, j, object_to_add):
        self.__game_map[i][j].append(object_to_add)
        self.__solid_sprite_group.add(object_to_add)

    def __create_map_from_layout(self):
        for i in range(self.__MAP_SIZE):
            for j in range(self.__MAP_SIZE):

                self.__game_map[i][j] = []
                self.__game_map[i][j].append(Grass(i * 32 + i + 32, j * 32 + j + 32))

                if self.__mapLayoutFile[i][j] == "1":
                    self.__game_map[i][j].append(Road(i * 32 + i + 32, j * 32 + j + 32))
                elif self.__mapLayoutFile[i][j] == "2":
                    self.__tractor.set_rect_by_index((i, j))
                elif self.__mapLayoutFile[i][j] == "3":
                    temp = Plant(i * 32 + i + 32, j * 32 + j + 32)
                    self.__game_map[i][j].append(temp)
                    self.__plants_sprite_group.add(temp)
                elif self.__mapLayoutFile[i][j] == "4":
                    self.__create_solid_object(i, j, Tree(i * 32 + i + 32, j * 32 + j + 32))
                elif self.__mapLayoutFile[i][j] == "5":
                    self.__create_solid_object(i, j, Barn(i * 32 + i + 32, j * 32 + j + 32))
                elif self.__mapLayoutFile[i][j] == "6":
                    self.__create_solid_object(i, j, WaterContainer(i * 32 + i + 32, j * 32 + j + 32))

    def render(self, hScreen):
        # grey background
        hScreen.fill([100, 100, 100])

        # black background beneath map grid to make lines more visible
        pygame.draw.rect(hScreen, [0, 0, 0], (30, 30, 33 * self.__MAP_SIZE + 3, 33 * self.__MAP_SIZE + 3))

        self.__render_interface(hScreen)

        # render sprites groups
        self.__ground_sprite_group.draw(hScreen)
        self.render_tractor(hScreen)

    def render_tractor(self, hScreen):
        self.__tractor_sprite_group.draw(hScreen)

    def __render_text_header_surface(self, font, colour, string_name, position_x, position_y, hScreen):
        name_surface = font.render(
            string_name,
            True,
            colour
        )
        hScreen.blit(name_surface, (position_x * 33, position_y * 33))

    def __render_stats_surface(self, dict, font, colour, position_x, position_y, hScreen):
        iterator_over_stat_dict_key = 0
        for stat in dict.keys():
            stats_surface = font.render(
                str(stat) + ": "
                + str(dict.get(stat)["level"])
                + "%",
                True,
                colour
            )

            hScreen.blit(stats_surface, (position_x * 33, position_y * 33 + iterator_over_stat_dict_key * 33))
            iterator_over_stat_dict_key += 1

    def __render_interface(self, hScreen):
        self.__render_ground_stats_interface(hScreen)
        self.__render_tractor_stats_interface(hScreen)
        self.__render_inventory_interface(hScreen)

    def __render_ground_stats_interface(self, hScreen):

        local_field_list = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        self.__render_text_header_surface(
            self.__ground_text_header_font,
            self.__ground_text_header_colour,
            local_field_list[len(local_field_list) - 1].get_name(),
            self.__MAP_SIZE + 4, 1,
            hScreen
        )

        if isinstance(local_field_list[len(local_field_list) - 1], AbstractHarvestablePlants):
            self.__render_stats_surface(
                local_field_list[len(local_field_list) - 1].get_stats(),
                self.__ground_stats_font,
                self.__ground_stats_colour,
                self.__MAP_SIZE + 4, 2,
                hScreen
            )

    def __render_tractor_stats_interface(self, hScreen):
        self.__render_stats_surface(
            self.__tractor.get_stats(),
            self.__tractor_stats_font,
            self.__tractor_stats_colour,
            1, self.__MAP_SIZE + 3,
            hScreen
        )

        self.__render_text_header_surface(
            self.__tractor_text_header_font,
            self.__tractor_text_header_colour,
            "Tractor Storage",
            1, self.__MAP_SIZE + 2,
            hScreen
        )

    def __render_inventory_interface(self, hScreen):
        self.__render_text_header_surface(
            self.__inventory_text_header_font,
            self.__inventory_text_header_colour,
            "Inventory",
            self.__MAP_SIZE + 4, 10,
            hScreen
        )

        self.__render_text_header_surface(
            self.__inventory_title_font,
            self.__inventory_title_colour,
            "Plants held: " + str(self.__tractor.get_plants_held()) + "/3",
            self.__MAP_SIZE + 4, 11,
            hScreen
        )

        self.__render_text_header_surface(
            self.__inventory_title_font,
            self.__inventory_title_colour,
            "Plants delivered: " + str(self.__plant_score),
            self.__MAP_SIZE + 4, 12,
            hScreen
        )

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                offset = self.__tractor.get_rect().copy()

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
                elif event.key == K_SPACE:
                    self.harvest_plants()
                elif event.key == K_d:
                    self.deliver_plants()
                elif event.key == K_g:
                    self.refill_tractor()

                # global collision detection
                self.__check_tractor_collisions(offset)

    def __check_tractor_collisions(self, offset):
        if self.tractor_collision_detection():
            self.__tractor.set_rect(offset)

    def update_sprites(self):
        if (pygame.time.get_ticks() - self.__start_time) / 1000 > 1:
            self.__start_time = pygame.time.get_ticks()

            for plant in self.__plants_sprite_group:
                plant.grow()

        self.__plants_sprite_group.update()
        self.__tractor_sprite_group.update()

    def do_things(self):
        field = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
        index = len(field) - 1

        if isinstance(field[index], AbstractHarvestablePlants):

            for stat in self.__tractor.get_stats().keys():

                if self.__tractor.if_operation_possible(stat):
                    tractor_stat_rate = self.__tractor.get_stat_rate(stat)

                    if field[index].if_operation_possible(stat, tractor_stat_rate):
                        field[index].take_care(stat, tractor_stat_rate)
                        field[index].update()

                        self.__tractor.operation(stat, tractor_stat_rate)

    def tractor_collision_detection(self):
        flag = False

        for solid_object in self.__solid_sprite_group:
            if solid_object.is_collided_with(self.__tractor):
                flag = True

        return flag

    def refill_tractor(self):

        for stat in self.__tractor.get_stats().keys():
            if self.__tractor.if_refill_possible(stat):
                tractor_stat_rate = self.__tractor.get_stat_rate_refill(stat)
                self.__tractor.refill(stat, tractor_stat_rate)

    def harvest_plants(self):
        field = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
        index = len(field) - 1

        if isinstance(field[index], AbstractHarvestablePlants):

            if self.__tractor.get_plants_held() < 3 and field[index].is_grown():
                self.__tractor.harvest()
                field[index].kill()
                del field[index]

    def deliver_plants(self):
        self.__plant_score += self.__tractor.get_plants_held()
        self.__tractor.deliver()
