import copy
import pygame

from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from engine.EngineService import collision_detection
from engine.EngineService import update_tractor_position


class Dfs:
    def __init__(self,
                 game_map,
                 solid_sprite_group,
                 plant_score_goal,
                 tractor):

        self.__solid_sprite_group = solid_sprite_group
        self.__tractor_position_copy = copy.deepcopy(tractor.get_position())
        self.__step_counter = 0
        self.__plant_score = 0
        self.__plant_score_goal = plant_score_goal
        self.__tractor = tractor
        self.__start_time = pygame.time.get_ticks()
        self.__map = game_map
        self.__is_path_found = False
        self.__paths_list = None

    def run(self):
        self.find_path()
        print(self.__paths_list)
        self.__tractor.set_position(self.__tractor_position_copy)
        return self.__paths_list

    def find_path(self, plants_found=0, path=None):

        if path is None:
            path = []

        possible_steps = self.__find_path_next_step(plants_found, path)

        for step in possible_steps:

            if self.__is_path_found:
                return

            if len(path) != 0:
                if self.__prevent_movement_loop(path, step):
                    continue

            if step == "p":
                plants_found += 1

            path.append(step)
            self.__update(step)

            if plants_found == self.__plant_score_goal:
                self.__paths_list = path
                self.__is_path_found = True
                return



            self.find_path(plants_found, path)

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

    def __find_path_next_step(self, plants_found, path):
        possible_steps = []

        # check possible movement
        if self.__tractor.move_up():
            if not collision_detection(self.__tractor, self.__solid_sprite_group):
                possible_steps.append("U")
            self.__tractor.move_down()

        if self.__tractor.move_down():
            if not collision_detection(self.__tractor, self.__solid_sprite_group):
                possible_steps.append("D")
            self.__tractor.move_up()

        if self.__tractor.move_left():
            if not collision_detection(self.__tractor, self.__solid_sprite_group):
                possible_steps.append("L")
            self.__tractor.move_right()

        if self.__tractor.move_right():
            if not collision_detection(self.__tractor, self.__solid_sprite_group):
                possible_steps.append("R")
            self.__tractor.move_left()

        field = self.__map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        if isinstance(field[-1], AbstractHarvestablePlants) and len(path) > 0:
                if path[-1] != "p":
                    possible_steps.append("p")
                    plants_found += 1

        possible_steps = sorted(list(possible_steps), key=lambda x: (not x.islower(), x))

        print("Possible steps: " + str(possible_steps) + " plants found: " + str(plants_found))

        return possible_steps

    def __update(self, step):
        print(self.__step_counter)
        update_tractor_position(step, self.__tractor)
        self.__step_counter += 1
