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

        # todo remove
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

        # self.__dfs = Dfs(self,
        #                  self.__game_map,
        #                  self.__tractor,
        #                  self.__plant_score_goal,
        #                  self.__solid_sprite_group,
        #                  self.__barns,
        #                  self.__watercontainers)

        # self.__mode = "auto"
        #
        # self.__dfs_solutions = []
        # self.__best_dfs_solution = []
        # self.__dfs_current_steps = []

        self.__start_time = pygame.time.get_ticks()

    def __dfs(self):
        gamemap = copy.copy(self.__game_map)
        dfs = Dfs(self,
                  gamemap,
                  copy.copy(self.__tractor),
                  copy.copy(self.__plant_score_goal),
                  copy.copy(self.__solid_sprite_group),
                  self.__MAP_SIZE)

        dfs.run()

    def __init_map_manager(self, map_layout):
        # todo why
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

    # todo move to mapmanager
    def init_map(self):
        # self.__load_map_from_file(path_to_map_layout)
        self.__mapLayoutFile = self.map_manager.get_map_layout()

        # create game map from layout
        self.__game_map_init()


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

    # def __load_map_from_file(self, path):
    #   with open(path) as textfile:
    #      self.__mapLayoutFile = list(line.replace('\n', '').split(" ") for line in textfile)

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
        self.__render_mode(hScreen)

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
            self.__right_column_pos, 5,
            hScreen
        )

        yPos = 5
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
    def __render_mode(self, hScreen):
        self.__render_text_header_surface(
            self.__inventory_text_header_font,
            self.__inventory_text_header_colour,
            "Mode: " + self.__mode,
            1, self.__MAP_SIZE + 6,
            hScreen
        )

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
        if (pygame.time.get_ticks() - self.__start_time) / 1000 > 2:
            self.__start_time = pygame.time.get_ticks()

            for plant in self.__plants_sprite_group:
                plant.grow()

            self.__plants_sprite_group.update()
            self.__tractor_sprite_group.update()

    # TODO: change name
    def do_things(self, map, tractor):
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

    #
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

        if self.refill_collision_detection(tractor) == "BARN":
            refill_type = "fertilizer"
        elif self.refill_collision_detection(tractor) == "WATER":
            refill_type = "irrigation"

        for stat in tractor.get_stats().keys():
            if stat == refill_type and tractor.if_refill_possible(stat):
                tractor_stat_rate = tractor.get_stat_rate_refill(stat)
                tractor.refill(stat, tractor_stat_rate)

    def harvest_plants(self, map, tractor):
        field = map[tractor.get_index_x()][tractor.get_index_y()]

        for object in field:
            if isinstance(object, AbstractHarvestablePlants):
                # todo change 3 to var
                if tractor.get_plants_held() < 3 and object.is_grown():
                    tractor.harvest()
                    object.kill()
                    del object

    def deliver_plants(self, plant_score, tractor):
        plant_score += tractor.get_plants_held()
        tractor.deliver()
        return plant_score

        # todo to nie może by tak, trzeba ustawi jakiś limit

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

    # def handle_dfs(self):
    #
    #     map_copy = self.__game_map.copy()
    #     tractor = copy.copy(self.__tractor)
    #     map_copy[tractor.get_index_x()][tractor.get_index_y()].append(tractor)
    #     self.dfs_find(map_copy, [], tractor)
    #     # self.dfs_find(map_copy, self.__dfs_current_steps, tractor)
    #     print(self.__dfs_solutions)
    #
    # def dfs_find(self, grid, current_steps, tractor):
    #     if len(self.__dfs_solutions) == 1: #todo change
    #         print("abandon in __dfs_solutions == 1")
    #         return
    #
    #     if self.__plant_score == self.__plant_score_goal: #todo: change to sim var
    #         self.__dfs_solutions.append(current_steps)
    #         print("adding to solutions")
    #         return
    #
    #     if len(current_steps) > 1000:
    #         print("abandon in dfs_find")
    #         return
    #
    #     else:
    #         if len(current_steps) == 0:
    #             s = None
    #         else:
    #             s = current_steps[-1] #last element of the current steps list
    #
    #         for step in self.possible_steps(grid, s, tractor, self.__plant_score_goal):
    #             new_current_steps = current_steps
    #
    #             if len(self.__dfs_solutions) == 1:  # todo change
    #                 return
    #
    #             # if len(current_steps) > 700:
    #             #     print("abandon in possible_steps")
    #             #     continue
    #
    #             new_current_steps.append(step)
    #             new_grid = self.modify_grid(grid.copy(), step, tractor)
    #
    #             # if last_position == tractor.get_rect():
    #             #     return
    #
    #             self.dfs_find(new_grid, new_current_steps, tractor)
    #
    # def possible_steps(self, grid, last_step, tractor, plant_score_goal):
    #     steps = {"L", "R", "U", "D", "i", "f", "h", "e", "b", "w"}
    #
    #     if last_step in {"i", "f", "h", "e", "b", "w"}:
    #         steps.remove(last_step)
    #
    #     if last_step is None:
    #         pass
    #     else:
    #         if last_step == "L":
    #             steps.remove("R")
    #
    #         elif last_step == "R":
    #             steps.remove("L")
    #
    #         elif last_step == "U":
    #             steps.remove("D")
    #
    #         elif last_step == "D":
    #             steps.remove("U")
    #
    #     if tractor.move_up():
    #         if self.sim_tractor_collision_detection(tractor):
    #             try:
    #                 steps.remove("U")
    #             except:
    #                 pass
    #         tractor.move_down()
    #     else:
    #         try:
    #             steps.remove("U")
    #         except:
    #             pass
    #
    #     if tractor.move_down():
    #         if self.sim_tractor_collision_detection(tractor):
    #             try:
    #                 steps.remove("D")
    #             except:
    #                 pass
    #         tractor.move_up()
    #     else:
    #         try:
    #             steps.remove("D")
    #         except:
    #             pass
    #
    #     if tractor.move_left():
    #         if self.sim_tractor_collision_detection(tractor):
    #             try:
    #                 steps.remove("L")
    #             except:
    #                 pass
    #         tractor.move_right()
    #     else:
    #         try:
    #             steps.remove("L")
    #         except:
    #             pass
    #
    #     if tractor.move_right():
    #         if self.sim_tractor_collision_detection(tractor):
    #             try:
    #                 steps.remove("R")
    #             except:
    #                 pass
    #         tractor.move_left()
    #     else:
    #         try:
    #             steps.remove("R")
    #         except:
    #             pass
    #
    #     if not any(isinstance(sprite, Plant) for sprite in grid[tractor.get_index_x()][tractor.get_index_y()]):
    #         try:
    #             steps.remove("i")
    #             steps.remove("f")
    #             steps.remove("h")
    #         except:
    #             pass
    #     else:
    #         field = grid[tractor.get_index_x()][tractor.get_index_y()]
    #         index = 1
    #
    #         if isinstance(field[index], AbstractHarvestablePlants):
    #             stage = field[index].get_grow_stage()
    #             if stage == 0:
    #                 try:
    #                     steps.remove("f")
    #                     steps.remove("h")
    #                 except:
    #                     pass
    #             elif stage == 1:
    #                 try:
    #                     steps.remove("i")
    #                     steps.remove("h")
    #                 except:
    #                     pass
    #             elif stage == 2:
    #                 try:
    #                     steps.remove("i")
    #                     steps.remove("f")
    #                     steps.remove("h")
    #                 except:
    #                     pass
    #             elif stage == 3:
    #                 try:
    #                     steps.remove("i")
    #                     steps.remove("f")
    #                     # tractor.harvest()
    #                 except:
    #                     pass
    #
    #             if not field[index].has_warning_on("irrigation"):
    #                 try:
    #                     steps.remove("i")
    #                 except:
    #                     pass
    #
    #             if not field[index].has_warning_on("fertilizer"):
    #                 try:
    #                     steps.remove("f")
    #                 except:
    #                     pass
    #
    #     if tractor.get_plants_held() != plant_score_goal: # TODO change to var
    #         try:
    #             steps.remove("e")
    #         except:
    #             pass
    #
    #     if not tractor.if_operation_possible("irrigation"):
    #         try:
    #             steps.remove("i")
    #         except:
    #             pass
    #
    #     if not tractor.if_operation_possible("fertilizer"):
    #         try:
    #             steps.remove("f")
    #         except:
    #             pass
    #
    #     if self.refill_collision_detection(tractor) != "WATER":
    #         try:
    #             steps.remove("w")
    #         except:
    #             pass
    #     else:
    #         if not tractor.if_refill_possible("irrigation"):
    #             try:
    #                 steps.remove("w")
    #             except:
    #                 pass
    #
    #     if self.refill_collision_detection(tractor) != "BARN":
    #         try:
    #             steps.remove("e")
    #         except:
    #             pass
    #         try:
    #             steps.remove("b")
    #         except:
    #             pass
    #     else:
    #         if not tractor.if_refill_possible("fertilizer"):
    #             try:
    #                 steps.remove("b")
    #             except:
    #                 pass
    #
    #     if not steps:
    #         print("T posX: " + str(tractor.get_index_x()) + " posY: " + str(tractor.get_index_y()) + "\tPusta lista")
    #
    #         if last_step == "L":
    #             steps.add("R")
    #         elif last_step == "R":
    #             steps.add("L")
    #         elif last_step == "U":
    #             steps.add("D")
    #         elif last_step == "D":
    #             steps.add("U")
    #
    #     new_steps = sorted(list(steps), key=lambda x: (not x.islower(), x))
    #     print("T posX: " + str(tractor.get_index_x()) + " posY: " + str(tractor.get_index_y()), end="\t")
    #     print("New possible steps" + str(new_steps))
    #     return new_steps
    #
    # def modify_grid(self, grid, step, tractor):
    #     print("Movement: " + step)
    #
    #     if step == "L":
    #         tractor.move_left()
    #     elif step == "R":
    #         tractor.move_right()
    #     elif step == "U":
    #         tractor.move_up()
    #     elif step == "D":
    #         tractor.move_down()
    #
    #     if step == "i":
    #         self.do_things(grid, tractor)
    #     if step == "f":
    #         self.do_things(grid, tractor)
    #     if step == "h":
    #         self.harvest_plants(grid, tractor)
    #     if step == "e":
    #         self.deliver_plants(tractor)
    #     if step == "w":
    #         self.refill_tractor(tractor)
    #     if step == "b":
    #         self.refill_tractor(tractor)
    #
    #     self.sim_update_sprites(grid)
    #     return grid
    #
    # def sim_update_sprites(self, grid):
    #     if (pygame.time.get_ticks() - self.__start_time) / 2 > 1:
    #         self.__start_time = pygame.time.get_ticks()
    #
    #         for fields in grid:
    #             for field in fields:
    #                 for object in field:
    #                     if isinstance(object, AbstractHarvestablePlants):
    #                         object.grow()
    #                         object.handle_warnings(True)
