import _thread as threading
import copy
import time

import pygame

from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from entities.Tractor import Tractor


class Dfs:

    def __init__(self, engine,
                 plant_score_goal,
                 map_size,
                 plant_position_list):
        self.__mode = "auto"

        self.__wait_flag = True
        self.step_counter = 0
        self.__path_counter = 0
        self.current_steps_limit = 100

        self.__dfs_solutions = []
        self.__best_dfs_solution = []
        self.__dfs_current_steps = []

        self.__tractor = Tractor(map_size)

        self.__plant_score = 0
        self.__plant_score_goal = plant_score_goal

        self.__plant_position_list = plant_position_list

        self.__start_time = pygame.time.get_ticks()

        self.__engine = engine
        # todo change
        self.__map = self.__engine.init_map()

        self.__timer_thread = threading.start_new_thread(self.timer, (0, 0))
        self.__plants_update_thread = threading.start_new_thread(self.__update_plants, (0, 0))

        # new var
        self.__paths_list = []
        self.__plants_found = 0

    def reset_map(self):
        self.__map = self.__engine.init_map()

    def run(self):
        while len(self.__paths_list) < 2:
        # while len(self.__dfs_solutions) < 2:
            print("--------------PATH " + str(self.__path_counter))

            self.dfs_find2()
            # self.dfs_find(0, [])
            self.reset_map()
            self.step_counter = 0
            self.__plants_found = 0

            time.sleep(0.5 + 0.1 * self.__path_counter)

            self.__path_counter += 1

        print(self.__paths_list)

    def dfs_find(self, plant_score, current_steps):
        if len(self.__dfs_solutions) == 2:  # todo change
            print("abandon in __dfs_solutions == 1")
            return True

        if plant_score >= self.__plant_score_goal:
            self.__dfs_solutions.append(current_steps)
            print("adding to solutions out")
            return

        if len(current_steps) > self.current_steps_limit:
            print("abandon in dfs_find")
            return

        else:
            if len(current_steps) == 0:
                s = None
            else:
                s = current_steps[-1]  # last element of the current steps list

            for step in self.possible_steps2(s):
                # for step in self.possible_steps(s):

                # if steps' list is empty, ends path
                if not step:
                    return False

                if len(self.__dfs_solutions) == 2:  # todo change
                    return True

                tractor_last_position = copy.deepcopy(self.__tractor.get_position())
                self.update(step)

                # if step == "p":
                #     if self.__wait_flag:
                #     time.sleep(1)
                #         self.__wait_flag = False
                #     if current_steps[-1] == "p":
                #         current_steps.remove("p")

                current_steps.append(step)

                if self.__plant_score == self.__plant_score_goal:
                    tmp_current_steps = copy.deepcopy(current_steps)
                    self.__dfs_solutions.append(tmp_current_steps)
                    print("adding to solutions in")
                    self.__plant_score = 0
                    break

                # if step == "i" or step == "f":
                #     time.sleep(1)

                if len(current_steps) > self.current_steps_limit:
                    print("abandon in possible_steps")
                    break

                tmp_flag = self.dfs_find(plant_score, current_steps)
                if tmp_flag is None:
                    del current_steps[-1]
                    # undo movement
                    self.__tractor.set_position(tractor_last_position)

    def dfs_find2(self):
        self.__find_path(0, [])
        # find best

    def __find_path_next_step(self, plants_found, last_step):
        possible_steps = []

        # check possible movement
        if not last_step == "D":
            if self.__tractor.move_up():
                if not self.__engine.collision_detection(self.__tractor):
                    if not possible_steps.__contains__("U"):
                        possible_steps.append("U")
                self.__tractor.move_down()

        if not last_step == "U":
            if self.__tractor.move_down():
                if not self.__engine.collision_detection(self.__tractor):
                    if not possible_steps.__contains__("D"):
                        possible_steps.append("D")
                self.__tractor.move_up()

        if not last_step == "R":
            if self.__tractor.move_left():
                if not self.__engine.collision_detection(self.__tractor):
                    if not possible_steps.__contains__("L"):
                        possible_steps.append("L")
                self.__tractor.move_right()

        if not last_step == "L":
            if self.__tractor.move_right():
                if not self.__engine.collision_detection(self.__tractor):
                    if not possible_steps.__contains__("R"):
                        possible_steps.append("R")
                self.__tractor.move_left()

        field = self.__map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        if isinstance(field[-1], AbstractHarvestablePlants):
            possible_steps.append("p")
            plants_found += 1

        possible_steps = sorted(list(possible_steps), key=lambda x: (not x.islower(), x))

        print("Possible steps: " + str(possible_steps))

        return (possible_steps, plants_found)

    def __find_path(self, plants_found, path):
        if len(self.__paths_list) == 2:  # todo change
            print("break max __find_path")
            return True

        # prevent from reach out limit of recursion
        if len(path) > self.current_steps_limit:
            print("abandon in __find_path")
            return

        if plants_found >= self.__plant_score_goal:
            print("adding a new path")
            # self.__plants_found -= 1
            # prevent from adding path which already exists
            if not path in self.__paths_list:
                self.__paths_list.append(copy.copy(path))
            else:
                print("abandon in adding the new path. path already exists")
            return

        if len(path) == 0:
            s = None
        else:
            s = path[-1]  # last step

        tmp_var = self.__find_path_next_step(plants_found, s)

        for step in tmp_var[0]:

            # if steps' list is empty, ends path
            if not step:
                return False

            path.append(step)

            if tmp_var[1] >= self.__plant_score_goal:
                print("adding a new path")
                # self.__plants_found -= 1
                # prevent from adding path which already exists
                if not path in self.__paths_list:
                    self.__paths_list.append(copy.copy(path))
                else:
                    print("abandon in adding the new path. path already exists")
                return


            tractor_last_position = copy.deepcopy(self.__tractor.get_position())
            self.update(step)


            # if plant_score >= self.__plant_score_goal:
            #     print("adding a new path")
            #
            #     # prevent from adding path which already exists
            #     if not path in self.__paths_list:
            #         self.__paths_list.append(path)
            #     else:
            #         print("abandon in adding the new path. path already exists")
            #     return

            if len(path) > self.current_steps_limit:
                print("abandon in possible_steps")
                break

            self.__find_path(tmp_var[1] , path)
            # tmp_flag = self.__find_path(plant_score, path)
            # if tmp_flag is None:
            del path[-1]

            #     undo movement
            self.__tractor.set_position(tractor_last_position)

    def possible_steps(self, last_step):
        steps = {"L", "R", "U", "D", "i", "f", "h", "e", "b", "w"}
        # steps = {"L", "R", "U", "D", "i", "f", "h", "e", "b", "w", "p"}

        grid = copy.copy(self.__map)

        if last_step in {"i", "f", "h", "e", "b", "w"}:
            steps.remove(last_step)

        if last_step is None:
            pass
        else:
            if last_step == "L":
                steps.remove("R")

            elif last_step == "R":
                steps.remove("L")

            elif last_step == "U":
                steps.remove("D")

            elif last_step == "D":
                steps.remove("U")

        if self.__tractor.move_up():
            if self.__engine.collision_detection(self.__tractor):
                try:
                    steps.remove("U")
                except:
                    pass
            self.__tractor.move_down()
        else:
            try:
                steps.remove("U")
            except:
                pass

        if self.__tractor.move_down():
            if self.__engine.collision_detection(self.__tractor):
                try:
                    steps.remove("D")
                except:
                    pass
            self.__tractor.move_up()
        else:
            try:
                steps.remove("D")
            except:
                pass

        if self.__tractor.move_left():
            if self.__engine.collision_detection(self.__tractor):
                try:
                    steps.remove("L")
                except:
                    pass
            self.__tractor.move_right()
        else:
            try:
                steps.remove("L")
            except:
                pass

        if self.__tractor.move_right():
            if self.__engine.collision_detection(self.__tractor):
                try:
                    steps.remove("R")
                except:
                    pass
            self.__tractor.move_left()
        else:
            try:
                steps.remove("R")
            except:
                pass

        field = grid[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        if not any(isinstance(sprite, AbstractHarvestablePlants) for sprite in
                   field):
            try:
                steps.remove("i")
                steps.remove("f")
                steps.remove("h")
                # steps.remove("p")
            except:
                pass
        else:
            # todo change field[1] to field[last elem]
            # if isinstance(field[1], AbstractHarvestablePlants):
            stage = field[1].get_grow_stage()
            if stage == 0:
                try:
                    steps.remove("f")
                    steps.remove("h")
                except:
                    pass
            elif stage == 1:
                try:
                    steps.remove("i")
                    steps.remove("h")
                except:
                    pass
            elif stage == 2:
                try:
                    steps.remove("i")
                    steps.remove("f")
                    steps.remove("h")
                except:
                    pass
            elif stage == 3:
                try:
                    steps.remove("i")
                    steps.remove("f")
                    # steps.remove("p")
                except:
                    pass

            if not field[1].has_warning_on("irrigation"):
                try:
                    steps.remove("i")
                except:
                    pass
            else:
                if not self.__tractor.if_operation_possible("irrigation"):
                    try:
                        steps.remove("i")
                        # steps.remove("p")
                    except:
                        pass
                # else:
                #     steps.remove("p")

            if not field[1].has_warning_on("fertilizer"):
                try:
                    steps.remove("f")
                except:
                    pass
            else:
                if not self.__tractor.if_operation_possible("fertilizer"):
                    try:
                        steps.remove("f")
                        # steps.remove("p")
                    except:
                        pass
                # else:
                #     steps.remove("p")

        if self.__tractor.get_plants_held() != self.__plant_score_goal:
            try:
                steps.remove("e")
            except:
                pass

        if self.__engine.refill_collision_detection(self.__tractor) != "WATER_CONTAINER":
            try:
                steps.remove("w")
            except:
                pass
        else:
            if not self.__tractor.if_refill_possible("irrigation"):
                try:
                    steps.remove("w")
                except:
                    pass

        if self.__engine.refill_collision_detection(self.__tractor) != "BARN":
            try:
                steps.remove("e")
            except:
                pass
            try:
                steps.remove("b")
            except:
                pass
        else:
            if not self.__tractor.if_refill_possible("fertilizer"):
                try:
                    steps.remove("b")
                except:
                    pass

        # todo perhaps to remove
        if not steps:
            print(
                "T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(
                    self.__tractor.get_index_y()) + "\tNone")
            return []


        new_steps = sorted(list(steps), key=lambda x: (not x.islower(), x))
        print("T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(self.__tractor.get_index_y()), end="\t")
        print("Possible steps: " + str(new_steps))
        return new_steps

    def possible_steps2(self, last_step):
        steps = []

        # check possible movement
        if not last_step == "D":
            if self.__tractor.move_up():
                if not self.__engine.collision_detection(self.__tractor):
                    if not steps.__contains__("U"):
                        steps.append("U")
                self.__tractor.move_down()

        if last_step == "U":
            if self.__tractor.move_down():
                if not self.__engine.collision_detection(self.__tractor):
                    if not steps.__contains__("D"):
                        steps.append("D")
                self.__tractor.move_up()

        if not last_step == "R":
            if self.__tractor.move_left():
                if not self.__engine.collision_detection(self.__tractor):
                    if not steps.__contains__("L"):
                        steps.append("L")
                self.__tractor.move_right()

        if not last_step == "L":
            if self.__tractor.move_right():
                if not self.__engine.collision_detection(self.__tractor):
                    if not steps.__contains__("R"):
                        steps.append("R")
                self.__tractor.move_left()

        field = self.__map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]

        # possible actions for plants
        if isinstance(field[-1], AbstractHarvestablePlants):
            self.__check_possible_plants(steps)
        #     plant = field[-1]
        #     stage = field[1].get_grow_stage()
        #
        #     if stage == 0:
        #         if plant.has_warning_on("irrigation") \
        #                 and self.__tractor.if_operation_possible("irrigation"):
        #             steps.append("i")
        #
        #     elif stage == 1:
        #         if plant.has_warning_on("fertilizer") \
        #                 and self.__tractor.if_operation_possible("fertilizer"):
        #             steps.append("f")
        #
        #     elif stage == 3:
        #         steps.append("h")
        #
        #     if not {"i", "f", "h"} in steps:
        #         steps.append("p")
        #
        # if self.__tractor.get_plants_held() == self.__plant_score_goal:
        #         steps.append("e")

        # todo add refill func

        # if self.__tractor.get_plants_held() == self.__plant_score_goal:
        #     steps.append("e")

        steps = sorted(list(steps), key=lambda x: (not x.islower(), x))

        print("T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(self.__tractor.get_index_y()), end="\t")
        print("Possible steps: " + str(steps))

        return steps

    def __check_possible_plants(self, steps):
        field = self.__map[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
        plant = field[-1]
        stage = field[1].get_grow_stage()

        if stage == 0:
            if plant.has_warning_on("irrigation") \
                    and self.__tractor.if_operation_possible("irrigation"):
                steps.append("i")

        elif stage == 1:
            if plant.has_warning_on("fertilizer") \
                    and self.__tractor.if_operation_possible("fertilizer"):
                steps.append("f")

        elif stage == 3:
            steps.append("h")

        if not {"i", "f", "h"} in steps:
            steps.append("p")

    def __update_tractor_position(self, movement):
        print(str(self.step_counter) + ". Movement: " + movement)
        self.step_counter += 1

        if movement == "L":
            self.__tractor.move_left()
        elif movement == "R":
            self.__tractor.move_right()
        elif movement == "U":
            self.__tractor.move_up()
        elif movement == "D":
            self.__tractor.move_down()

    def __update_map(self, step):

        # print(str(self.step_counter) + ". Movement: " + step)
        self.step_counter += 1

        self.__update_tractor_position(step)

        if step == "i" or step == "f":
            self.__engine.do_things(self.__map, self.__tractor)

        # if tractor stay next to plant and cannot irrigate/fertilize/harvest, sleeps for 1 sec
        # if step == "p":
        #     time.sleep(1)

        if step == "h":
            self.__engine.harvest_plants(self.__map, self.__tractor)
        if step == "e":

            self.set_plant_score(
                self.__engine.deliver_plants(self.__plant_score, self.__tractor)
            )

        if step == "w" or step == "b":
            self.__engine.refill_tractor(self.__tractor)

    def update(self, step):
        self.__update_map(step)

    def __update_plants(self, a, b):
        while True:
            if (pygame.time.get_ticks() - self.__start_time) / 1000 > 2:
                self.__start_time = pygame.time.get_ticks()

                for fields in self.__map:
                    for field in fields:
                        for entity in field:
                            if isinstance(entity, AbstractHarvestablePlants):
                                entity.grow()
                                entity.handle_warnings(True)
            time.sleep(1)

    def timer(self, a, b):
        while True:
            if self.__engine.get_pause_flag():
                time.sleep(2)
                self.__engine.set_pause_flag(False)
            else:
                time.sleep(1.75)

    def set_plant_score(self, plant_score):
        self.__plant_score = plant_score
