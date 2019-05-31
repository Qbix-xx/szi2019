import sys
import time

import pygame
from pygame.locals import *

from engine.EngineService import collision_detection
from engine.EngineService import update_tractor_position
from engine.GUI import GUI
from entities.Barn import Barn
from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from entities.Tractor import Tractor
from entities.WaterContainer import WaterContainer
from .MapManager import MapManager
from .algor.Dfs import Dfs


class Engine:
    def __init__(self, widow_size):
        self.__widow_size = widow_size
        self.__hScreen = pygame.display.set_mode(self.__widow_size)
        GUI.set_hScreen(self.__hScreen)
        self.__init_map_manager("layout3_dev.txt")
        self.__MAP_SIZE = self.__map_manager.get_map_size()
        self.__barns_list = []
        self.__water_containers_list = []
        self.__init_sprites()
        self.__mapLayoutFile = None
        self.__game_map = None
        self.init_map()
        self.__selected_map_idx = self.__map_manager.get_map_idx()
        self.__plants_score = 0
        self.__plant_score_goal = len(self.__plants_sprite_group.sprites())
        self.__plant_position_list = []
        self.__start_time = pygame.time.get_ticks()
        GUI.set_map_size(self.__MAP_SIZE)

    def __map_reset(self, map_layout):
        self.__hScreen = pygame.display.set_mode(self.__widow_size)
        GUI.set_hScreen(self.__hScreen)
        self.__init_map_manager(map_layout)
        self.__MAP_SIZE = self.__map_manager.get_map_size()
        self.__barns_list = []
        self.__water_containers_list = []
        self.__init_sprites()
        self.init_map()
        self.__selected_map_idx = self.__map_manager.get_map_idx()
        self.__plants_score = 0
        self.__plant_score_goal = len(self.__plants_sprite_group.sprites())
        self.__plant_position_list = []
        self.__start_time = pygame.time.get_ticks()
        GUI.set_map_size(self.__MAP_SIZE)
        self.__plants_sprite_group.update()

    def __dfs(self):
        dfs = Dfs(self.__game_map,
                  self.__solid_sprite_group,
                  self.__plant_score_goal,
                  self.__tractor)

        path = dfs.run()
        final_path = self.adjust_and_expand_path(path)
        print("Final path: ", final_path)
        self.auto_movement(final_path)

    def adjust_and_expand_path(self, path):
        for index, step in enumerate(path):
            if path[index] == "p":
                path[index] = "i"

        final_path = path.copy()
        final_path.extend(self.trim_and_reverse_path(path).copy())
        final_path.extend(self.trim_and_reverse_path(path).copy())
        # TODO
        # first_plant_index = next((i for i, step in enumerate(path) if step == "i"), None)
        # final_path[first_plant_index] = wait for the first plant to get irrigation warning (p, ..., p, i)
        # add (go back to the barn and deliver plants) part at the end of final_path
        return final_path

    def trim_and_reverse_path(self, path):
        start = next((i for i, step in enumerate(path) if step == "i" or step == "f"), None)

        # delete the part where tractor goes from starting point to the first plant
        del path[:start]

        path.reverse()

        for index, step in enumerate(path):
            if path[index] == "U":
                path[index] = "D"
            elif path[index] == "D":
                path[index] = "U"
            elif path[index] == "L":
                path[index] = "R"
            elif path[index] == "R":
                path[index] = "L"
            elif path[index] == "i":
                path[index] = "f"
            elif path[index] == "f":
                path[index] = "h"

        return path

    def auto_movement(self, path):
        step_counter = 0
        for step in path:
            print(str(step_counter) + ". ", end='')
            update_tractor_position(step, self.__tractor)
            self.render()
            pygame.display.flip()

            time.sleep(0.5)
            step_counter += 1

    def __init_map_manager(self, map_layout):
        self.__map_manager = MapManager()
        try:
            self.__map_manager.load_map(map_layout)
        except:
            print("Couldn't load map: " + self.__map_manager.get_map_name())

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
        self.__mapLayoutFile = self.__map_manager.get_map_layout()
        self.__game_map_init()

        return self.__game_map

    def __game_map_init(self):
        self.__game_map = self.__map_manager.create_map_from_layout(
            self.__tractor,
            self.__solid_sprite_group,
            self.__plants_sprite_group,
            self.__water_containers_list,
            self.__barns_list
        )

        self.__ground_sprite_group.add(self.__game_map)

    def __create_solid_object(self, i, j, object_to_add):
        self.__game_map[i][j].append(object_to_add)
        self.__solid_sprite_group.add(object_to_add)

    def render(self):
        GUI.render_interface(self.__game_map[self.__tractor.get_index_x()][self.__tractor.get_index_y()],
                             self.__tractor.get_stats(),
                             self.__tractor.get_plants_held(),
                             self.__plants_score,
                             self.__map_manager)

        self.__ground_sprite_group.draw(self.__hScreen)
        self.__tractor_sprite_group.draw(self.__hScreen)

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:

                if event.key == K_RIGHT:
                    self.__tractor.move_right()
                    if collision_detection(self.__tractor, self.__solid_sprite_group):
                        self.__tractor.move_left()
                elif event.key == K_LEFT:
                    self.__tractor.move_left()
                    if collision_detection(self.__tractor, self.__solid_sprite_group):
                        self.__tractor.move_right()
                elif event.key == K_DOWN:
                    self.__tractor.move_down()
                    if collision_detection(self.__tractor, self.__solid_sprite_group):
                        self.__tractor.move_up()
                elif event.key == K_UP:
                    self.__tractor.move_up()
                    if collision_detection(self.__tractor, self.__solid_sprite_group):
                        self.__tractor.move_down()

                if event.key == K_f:
                    self.do_things(self.__game_map, self.__tractor)
                elif event.key == K_SPACE:
                    self.harvest_plants(self.__game_map, self.__tractor)
                elif event.key == K_d:
                    self.deliver_plants(self.__plants_score, self.__tractor)
                elif event.key == K_g:
                    self.refill_tractor(self.__tractor)

                elif event.key == K_x:
                    self.__map_manager.decrease_map_idx()
                elif event.key == K_z:
                    self.__map_manager.increase_map_idx()
                elif event.key == K_RETURN:
                    self.__map_reset(self.__map_manager.get_map_layout_name_with_selected_idx())
                elif event.key == K_m:
                    self.__dfs()

    def update(self):
        if (pygame.time.get_ticks() - self.__start_time) / 1000 > 1:
            self.__start_time = pygame.time.get_ticks()

            for plant in self.__plants_sprite_group:
                plant.grow()

            self.__plants_sprite_group.update()

    # TODO: change name
    def do_things(self, game_map, tractor):
        field = game_map[tractor.get_index_x()][tractor.get_index_y()]

        for plant in field:
            if isinstance(plant, AbstractHarvestablePlants):
                for stat in tractor.get_stats().keys():

                    if tractor.if_operation_possible(stat):
                        tractor_stat_rate = tractor.get_stat_rate(stat)

                        if plant.if_operation_possible(stat, tractor_stat_rate):
                            plant.take_care(stat, tractor_stat_rate)
                            plant.update()

                            tractor.operation(stat, tractor_stat_rate)

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

        for plant in field:
            if isinstance(plant, AbstractHarvestablePlants):

                # todo remove storage limit from project
                if plant.is_grown():
                    # if tractor.get_plants_held() < 3 and plant.is_grown():
                    tractor.harvest()
                    plant.kill()
                    del plant

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

    def get_plants_group(self):
        return self.__plants_sprite_group
