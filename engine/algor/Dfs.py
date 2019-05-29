import copy

import pygame

from engine.EngineService import collision_detection
from engine.EngineService import update_tractor_position
from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from entities.Tractor import Tractor


class Dfs:
    def __init__(self,
                 game_map,
                 solid_sprite_group,
                 plant_score_goal,
                 tractor: Tractor):

        self.__solid_sprite_group = solid_sprite_group
        self.__tractor_position_copy = copy.deepcopy(tractor.get_position())
        self.__plant_score_goal = plant_score_goal
        self.__tractor = tractor
        self.__start_time = pygame.time.get_ticks()
        self.__game_map = game_map
        self.__paths_list = []
        self.__path_nodes = []

    def run(self):
        self.find_path(self.__tractor)
        self.__tractor.set_position(self.__tractor_position_copy)
        self.__print_path_list()

        return self.__find_shortest_path()

    def __print_path_list(self):
        print("Found paths: ")
        counter = 1

        for path in self.__paths_list:
            print(str(counter) + ". " + str(path))
            counter += 1

    def __find_shortest_path(self):
        best_path = []

        for path in self.__paths_list:
            if len(best_path) == 0:
                best_path = copy.deepcopy(path)
                continue

            if len(best_path) > len(path):
                best_path = copy.deepcopy(path)

        print("Best path: " + str(best_path))

        return best_path

    def find_path(self, tractor: Tractor, step_counter=0, plants_found=0,
                  path=None,
                  plants_found_list=None,
                  path_nodes=None):

        if path is None:
            path = []

        if plants_found_list is None:
            plants_found_list = []

        if path_nodes is None:
            path_nodes = [self.__tractor.get_index()]

        possible_steps = self.__find_path_next_step(tractor, plants_found, path, plants_found_list)

        for step in possible_steps:

            if len(path) != 0:
                if self.__prevent_movement_loop(path, step):
                    continue

            if step == "p":
                plants_found += 1

            path.append(step)
            tractor_position_copy = copy.deepcopy(self.__tractor.get_position())
            step_counter = self.__update(step, step_counter, tractor)
            path_nodes.append(self.__tractor.get_index())

            path_length = len(path)

            if path_length % 5 == 0:
                current_pos = path_nodes[-1]
                pos_to_check = path_nodes[path_length - 4]

                if current_pos == pos_to_check:
                    print("found loop in path")
                    tractor.set_position(tractor_position_copy)
                    del path[-1]
                    step_counter -= 1
                    del path_nodes[-1]

                    continue

            if path.count("p") == self.__plant_score_goal:
                self.__paths_list.append(copy.deepcopy(path))
                print("Adding path: " + str(path))
                del plants_found_list[-1]
                del path[-1]
                del path_nodes[-1]

                return

            self.find_path(tractor, step_counter, plants_found, path, plants_found_list, path_nodes)

            if step == "p":
                del plants_found_list[-1]

            step_counter -= 1
            del path[-1]
            del path_nodes[-1]
            tractor.set_position(tractor_position_copy)

    @staticmethod
    def __prevent_movement_loop(path, possible_step):
        last_step = path[-1]
        flag = False

        if possible_step == "R":
            if last_step == "L":
                flag = True
        elif possible_step == "L":
            if last_step == "R":
                flag = True
        elif possible_step == "U":
            if last_step == "D":
                flag = True
        elif possible_step == "D":
            if last_step == "U":
                flag = True

        return flag

    def __find_path_next_step(self, tractor, plants_found, path, plants_found_list):
        possible_steps = []

        # check possible movement
        if tractor.move_up():
            if not collision_detection(tractor, self.__solid_sprite_group):
                possible_steps.append("U")
            tractor.move_down()

        if tractor.move_down():
            if not collision_detection(tractor, self.__solid_sprite_group):
                possible_steps.append("D")
            tractor.move_up()

        if tractor.move_left():
            if not collision_detection(tractor, self.__solid_sprite_group):
                possible_steps.append("L")
            tractor.move_right()

        if tractor.move_right():
            if not collision_detection(tractor, self.__solid_sprite_group):
                possible_steps.append("R")
            tractor.move_left()

        field = self.__game_map[tractor.get_index_x()][tractor.get_index_y()]

        if isinstance(field[-1], AbstractHarvestablePlants) and len(path) > 0:
            if field[-1] not in plants_found_list:
                if path[-1] != "p":
                    possible_steps.append("p")
                    plants_found += 1
                    plants_found_list.append(field[-1])

        possible_steps = sorted(list(possible_steps), key=lambda x: (not x.islower(), x))

        print("Actual path: " + str(path))
        print("Possible steps: " + str(possible_steps) + " plants found: " + str(plants_found))

        return possible_steps

    def __update(self, step, step_counter, tractor: Tractor):
        print("Step number: " + str(step_counter))
        print("-----------------------")
        update_tractor_position(step, tractor)

        if step != "p":
            step_counter += 1

        return step_counter
