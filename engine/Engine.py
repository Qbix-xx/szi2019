import copy
import os
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
from .MapManager import MapManager
from .algor.Dfs import Dfs


class Engine:
    def __init__(self, map_layout):
        self.__game_init(map_layout)

    def __game_init(self, map_layout):
        self.__init_map_manager(map_layout)
        self.__MAP_SIZE = self.map_manager.get_map_size()

        self.__barns = []
        self.__water_containers = []

        self.__set_fonts_and_colours()

        self.__mode = "auto"

        self.__pause_flag = False

        self.__init_sprites()
        self.init_map()
        self.__selected_map_idx = self.map_manager.get_map_idx()

        # plants delivered in total
        self.__plant_score = 0
        self.__plant_score_goal = len(self.__plants_sprite_group.sprites())

        self.__plant_position_list = []

        self.__start_time = pygame.time.get_ticks()

    def __dfs(self):
        dfs = Dfs(self,
                  copy.copy(self.__plant_score_goal),
                  self.__MAP_SIZE,
                  self.__plant_position_list)

        dfs.run()

    def __init_map_manager(self, map_layout):
        # todo why os path join
        self.map_manager = MapManager(
            os.path.join("resources", "map_layouts"),
            map_layout)
        try:
            self.map_manager.load_map("default")

        except:
            print("Couldn't load map: " + self.map_manager.get_map_name())

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

    def init_map(self):
        self.__mapLayoutFile = self.map_manager.get_map_layout()

        # create game map from layout
        self.__game_map_init()
        return self.__game_map
        # return (self.__game_map, self)

    def __set_fonts_and_colours(self):
        self.__ground_text_header_font = pygame.font.SysFont('showcardgothic', 30)
        self.__ground_text_header_colour = (0, 0, 0)
        self.__ground_stats_font = pygame.font.SysFont('unispacebold', 20)
        self.__ground_stats_colour = (0, 0, 0)

        self.__tractor_text_header_font = pygame.font.SysFont('showcardgothic', 30)
        self.__tractor_text_header_colour = (0, 0, 0)
        self.__tractor_stats_font = pygame.font.SysFont('unispacebold', 20)
        self.__tractor_stats_colour = (0, 0, 0)

        self.__inventory_text_header_font = pygame.font.SysFont('showcardgothic', 30)
        self.__inventory_text_header_colour = (0, 0, 0)
        self.__inventory_title_font = pygame.font.SysFont('unispacebold', 20)
        self.__inventory_title_colour = (0, 0, 0)

        self.__current_map_color = (220, 20, 60)
        self.__selected_map_color = (255, 215, 0)

        map_manager_map_size = self.map_manager.get_map_size()

        if map_manager_map_size < 10:
            dif = 15 - map_manager_map_size + 2
            self.__right_column_pos = map_manager_map_size + dif
        else:
            self.__right_column_pos = map_manager_map_size + 4

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
                    # x = i * 32 + i + 32
                    # y = j * 32 + j + 32
                    # temp = Plant(x, y)
                    # self.__plant_position_list.append((x, y))
                    temp = Plant(i * 32 + i + 32, j * 32 + j + 32)
                    self.__game_map[i][j].append(temp)
                    self.__plants_sprite_group.add(temp)
                elif self.__mapLayoutFile[i][j] == "4":
                    self.__create_solid_object(i, j, Tree(i * 32 + i + 32, j * 32 + j + 32))
                elif self.__mapLayoutFile[i][j] == "5":
                    self.__barns.append(Barn(i * 32 + i + 32, j * 32 + j + 32))
                    self.__create_solid_object(i, j, self.__barns[len(self.__water_containers) - 1])
                elif self.__mapLayoutFile[i][j] == "6":
                    self.__water_containers.append(WaterContainer(i * 32 + i + 32, j * 32 + j + 32))
                    self.__create_solid_object(i, j, self.__water_containers[len(self.__water_containers) - 1])

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
                + str(dict.get(stat)),
                True,
                colour
            )

            hScreen.blit(stats_surface, (position_x * 33, position_y * 33 + iterator_over_stat_dict_key * 33))
            iterator_over_stat_dict_key += 1

    def __render_interface(self, hScreen):
        self.__render_ground_stats_interface(hScreen)
        self.__render_tractor_stats_interface(hScreen)
        self.__render_inventory_interface(hScreen)
        self.__render_map_list(hScreen)
        # self.__render_mode(hScreen)

    def __render_ground_stats_interface(self, hScreen):

        local_field_list = self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        self.__render_text_header_surface(
            self.__ground_text_header_font,
            self.__ground_text_header_colour,
            local_field_list[len(local_field_list) - 1].get_name(),
            self.__right_column_pos, 1,
            hScreen
        )

        if isinstance(local_field_list[len(local_field_list) - 1], AbstractHarvestablePlants):
            temp_stats = local_field_list[len(local_field_list) - 1].get_stats()
            plant_stage = local_field_list[len(local_field_list) - 1].get_grow_stage()

            dict_to_display = {
                "Watered": temp_stats["irrigation"]["done"],
                "Fertilized": temp_stats["fertilizer"]["done"],
                "Growth stage": plant_stage + 1,
                "irrigation": temp_stats["irrigation"]["level"],
                "fertilizer": temp_stats["fertilizer"]["level"]
            }

            self.__render_stats_surface(
                dict_to_display,
                self.__ground_stats_font,
                self.__ground_stats_colour,
                self.__right_column_pos, 2,
                hScreen
            )

    def __render_tractor_stats_interface(self, hScreen):

        temp_stats = self.__tractor.get_stats()

        dict_to_display = {
            "irrigation": temp_stats["irrigation"]["level"],
            "fertilizer": temp_stats["fertilizer"]["level"]
        }

        self.__render_stats_surface(
            dict_to_display,
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
            10, self.__MAP_SIZE + 2,
            hScreen
        )

        self.__render_text_header_surface(
            self.__inventory_title_font,
            self.__inventory_title_colour,
            "Plants held: " + str(self.__tractor.get_plants_held()) + "/3",
            10, self.__MAP_SIZE + 3,
            hScreen
        )

        self.__render_text_header_surface(
            self.__inventory_title_font,
            self.__inventory_title_colour,
            "Plants delivered: " + str(self.__plant_score),
            10, self.__MAP_SIZE + 4,
            hScreen
        )

    def __render_map_list(self, hScreen):
        maps = self.map_manager.get_map_list()
        self.__render_text_header_surface(
            self.__inventory_text_header_font,
            self.__inventory_text_header_colour,
            "Map list",
            self.__right_column_pos, 10,
            hScreen
        )

        yPos = 10
        for map in maps:
            yPos = yPos + 1
            if map == self.map_manager.get_map_name():
                color = self.__current_map_color
            elif map == maps[self.__selected_map_idx]:
                color = self.__selected_map_color
            else:
                color = self.__inventory_title_colour
            self.__render_text_header_surface(
                self.__inventory_title_font,
                color,
                map,
                self.__right_column_pos, yPos,
                hScreen
            )

    # todo remove
    # def __render_mode(self, hScreen):
    #     self.__render_text_header_surface(
    #         self.__inventory_text_header_font,
    #         self.__inventory_text_header_colour,
    #         "Mode: " + self.__mode,
    #         1, self.__MAP_SIZE + 6,
    #         hScreen
    #     )

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                offset = self.__tractor.get_rect().copy()

                if not self.__pause_flag:
                    if event.key == K_RIGHT:
                        self.__tractor.move_right()
                        self.__pause_flag = True
                    elif event.key == K_LEFT:
                        self.__tractor.move_left()
                        self.__pause_flag = True
                    elif event.key == K_DOWN:
                        self.__tractor.move_down()
                        self.__pause_flag = True
                    elif event.key == K_UP:
                        self.__tractor.move_up()
                        self.__pause_flag = True

                if event.key == K_f:
                    self.do_things(self.__game_map, self.__tractor)
                elif event.key == K_SPACE:
                    self.harvest_plants(self.__game_map, self.__tractor)
                elif event.key == K_d:
                    self.deliver_plants(self.__plant_score, self.__tractor)
                elif event.key == K_g:
                    self.refill_tractor(self.__tractor)

                elif event.key == K_x:
                    self.__selected_map_idx = self.__selected_map_idx - 1
                    if self.__selected_map_idx < 0:
                        self.__selected_map_idx = len(self.map_manager.get_map_list()) - 1
                elif event.key == K_z:
                    self.__selected_map_idx = self.__selected_map_idx + 1
                    if self.__selected_map_idx >= len(self.map_manager.get_map_list()):
                        self.__selected_map_idx = 0
                elif event.key == K_RETURN:
                    self.__game_init(
                        self.map_manager.get_map_layout_name_with_idx(self.__selected_map_idx))

                elif event.key == K_m:
                    self.__dfs()

                # global collision detection
                self.__check_tractor_collisions(offset)

    def __check_tractor_collisions(self, offset):
        if self.collision_detection(self.__tractor):
            self.__tractor.set_rect(offset)

    def update(self):
        if (pygame.time.get_ticks() - self.__start_time) / 1000 > 1:
            self.__start_time = pygame.time.get_ticks()

            for plant in self.__plants_sprite_group:
                plant.grow()

            self.__plants_sprite_group.update()
            self.__tractor_sprite_group.update()

    # TODO: change name
    def do_things(self, map, tractor):
        # todo change iteration to [-1]
        field = map[tractor.get_index_x()][tractor.get_index_y()]

        for object in field:
            if isinstance(object, AbstractHarvestablePlants):

                for stat in tractor.get_stats().keys():

                    if tractor.if_operation_possible(stat):
                        tractor_stat_rate = tractor.get_stat_rate(stat)

                        if object.if_operation_possible(stat, tractor_stat_rate):
                            object.take_care(stat, tractor_stat_rate)
                            object.update()

                            tractor.operation(stat, tractor_stat_rate)

    def collision_detection(self, sprite):
        flag = False

        for solid_object in self.__solid_sprite_group:
            if solid_object.is_collided_with(sprite):
                flag = True
                break

        return flag

    # def sim_tractor_collision_detection(self, tractor):
    #     flag = False
    #
    #     for solid_object in self.__solid_sprite_group:
    #         if solid_object.is_collided_with(tractor):
    #             flag = True
    #             break
    #
    #     return flag

    def refill_tractor(self, tractor):
        refill_type = None

        refill_collision = self.refill_collision_detection(tractor)

        if refill_collision == "BARN":
            refill_type = "fertilizer"
        elif refill_collision == "WATER_CONTAINER":
            refill_type = "irrigation"

        if refill_type is not None and tractor.if_refill_possible(refill_type):
            tractor.refill(refill_type, tractor.get_stat_rate_refill(refill_type))

        # for stat in tractor.get_stats().keys():
        #     if stat == refill_type and tractor.if_refill_possible(stat):
        #         tractor_stat_rate = tractor.get_stat_rate_refill(stat)
        #         tractor.refill(stat, tractor_stat_rate)

    def harvest_plants(self, map, tractor):
        field = map[tractor.get_index_x()][tractor.get_index_y()]

        for object in field:
            if isinstance(object, AbstractHarvestablePlants):

                # todo remove storage limit from project
                if object.is_grown():
                    # if tractor.get_plants_held() < 3 and object.is_grown():
                    tractor.harvest()
                    object.kill()
                    del object

    def deliver_plants(self, plant_score, tractor):
        plant_score += tractor.get_plants_held()
        tractor.deliver()
        return plant_score

        # todo should be possible only below specific level

    def refill_collision_detection(self, tractor):
        for sprite in self.__solid_sprite_group:
            if isinstance(sprite, (Barn, WaterContainer)):
                if sprite.get_refill_hitbox().colliderect(tractor.rect):
                    return sprite.get_name()

        return None

    def get_pause_flag(self):
        return self.__pause_flag

    def set_pause_flag(self, flag):
        self.__pause_flag = flag
