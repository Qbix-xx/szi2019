import _thread as threading
import copy
import time

import pygame

from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
from entities.Ground.Plant import Plant
from entities.Tractor import Tractor


class Dfs:
    def __init__(self, engine, game_map, tractor,
                 plant_score_goal, solid_sprite_group,
                 map_size):
        self.__mode = "auto"

        self.counter = 0
        self.current_steps_limit = 100

        self.__dfs_solutions = []
        self.__best_dfs_solution = []
        self.__dfs_current_steps = []

        self.__map = copy.copy(game_map)
        # self.__tractor = copy.copy(tractor)
        self.__tractor = Tractor(map_size)

        self.__plant_score = 0
        self.__plant_score_goal = plant_score_goal

        self.__solid_sprite_group = copy.copy(solid_sprite_group)

        self.__start_time = pygame.time.get_ticks()

        self.__timer_thread = threading.start_new_thread(self.timer, (0, 0))

        self.__engine = engine

        self.__engine.init_map()

    def run(self):
        self.dfs_find(0, [])

        print(self.__dfs_solutions)

    def dfs_find(self, plant_score, current_steps):
        if len(self.__dfs_solutions) == 1:  # todo change
            print("abandon in __dfs_solutions == 1")
            return

        if plant_score >= self.__plant_score_goal:
            self.__dfs_solutions.append(current_steps)
            print("adding to solutions")
            return

        if len(current_steps) > self.current_steps_limit:
            print("abandon in dfs_find")
            return

        else:
            if len(current_steps) == 0:
                s = None
            else:
                s = current_steps[-1]  # last element of the current steps list

            for step in self.possible_steps(s):
                temp_current_steps = current_steps

                if len(self.__dfs_solutions) == 1:  # todo change
                    return

                if self.__plant_score == self.__plant_score_goal:
                    self.__dfs_solutions.append(current_steps)
                    print("adding to solutions")
                    # self.__plant_score = 0
                    return



                if len(current_steps) > self.current_steps_limit:
                    print("abandon in possible_steps")
                    break

                temp_current_steps.append(step)
                self.update(step)

                self.dfs_find(plant_score, temp_current_steps)

    def possible_steps(self, last_step):
        steps = []
        grid = self.__map

        if self.__tractor.move_up():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("U")
            self.__tractor.move_down()

        if self.__tractor.move_down():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("D")
            self.__tractor.move_up()

        if self.__tractor.move_left():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("L")
            self.__tractor.move_right()

        if self.__tractor.move_right():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("R")
            self.__tractor.move_left()

        if last_step is None:
            pass
        else:
            if last_step == "L" and "R" in steps:
                steps.remove("R")

            elif last_step == "R" and "L" in steps:
                steps.remove("L")

            elif last_step == "U" and "D" in steps:
                steps.remove("D")

            elif last_step == "D" and "U" in steps:
                steps.remove("U")

        if any(isinstance(sprite, Plant) for sprite in
               grid[self.__tractor.get_index_x()][self.__tractor.get_index_y()]):
            field = grid[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
            index = 1  # because Plant is always at this index in field list (grass at 0)
            if isinstance(field[index], AbstractHarvestablePlants):
                stage = field[index].get_grow_stage()
                if stage == 0 and field[index].has_warning_on("irrigation") and\
                        self.__tractor.if_operation_possible("irrigation"):
                    steps.append("i")
                elif stage == 1 and field[index].has_warning_on("fertilizer") and\
                        self.__tractor.if_operation_possible("fertilizer"):
                    steps.append("f")
                elif stage == 2:
                    pass
                elif stage == 3 and self.__tractor.get_plants_held() < 3:
                    steps.append("h")

        if self.__engine.refill_collision_detection(self.__tractor) == "WATER_CONTAINER" and\
                self.__tractor.if_refill_possible("irrigation"):
                steps.append("w")

        if self.__engine.refill_collision_detection(self.__tractor) == "BARN":
                if self.__tractor.if_refill_possible("fertilizer"):
                    steps.append("b")
                if self.__tractor.get_plants_held() > 0:
                    steps.append("e")

        if not steps:
            print(
                "T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(
                    self.__tractor.get_index_y()) + "\tPusta lista")

            if last_step == "L":
                steps.append("R")
            elif last_step == "R":
                steps.append("L")
            elif last_step == "U":
                steps.append("D")
            elif last_step == "D":
                steps.append("U")

        new_steps = sorted(list(steps), key=lambda x: (not x.islower(), x))
        print("T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(self.__tractor.get_index_y()), end="\t")
        print("New possible steps" + str(new_steps))
        return new_steps

    def possible2(self, last_step):
        # steps = {"L", "R", "U", "D", "i", "f", "h", "e", "b", "w"}
        steps = []

        # if last_step is None:
        #     pass
        # else:
        #     if last_step == "L":
        #         steps.remove("R")
        #
        #     elif last_step == "R":
        #         steps.remove("L")
        #
        #     elif last_step == "U":
        #         steps.remove("D")
        #
        #     elif last_step == "D":
        #         steps.remove("U")

        if self.__tractor.move_up():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("U")
            self.__tractor.move_down()

        if self.__tractor.move_down():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("D")
            self.__tractor.move_up()

        if self.__tractor.move_left():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("L")
            self.__tractor.move_right()

        if self.__tractor.move_right():
            if not self.__engine.collision_detection(self.__tractor):
                steps.append("R")
            self.__tractor.move_left()

        if not any(isinstance(sprite, Plant) for sprite in
                   grid[self.__tractor.get_index_x()][self.__tractor.get_index_y()]):
            try:
                steps.remove("i")
                steps.remove("f")
                steps.remove("h")
            except:
                pass
        else:
            field = grid[self.__tractor.get_index_x()][self.__tractor.get_index_y()]
            index = 1

            if isinstance(field[index], AbstractHarvestablePlants):
                stage = field[index].get_grow_stage()
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
                    except:
                        pass

                if not field[index].has_warning_on("irrigation"):
                    try:
                        steps.remove("i")
                    except:
                        pass

                if not field[index].has_warning_on("fertilizer"):
                    try:
                        steps.remove("f")
                    except:
                        pass

        if self.__tractor.get_plants_held() != self.plant_score_goal:
            try:
                steps.remove("e")
            except:
                pass

        if not self.__tractor.if_operation_possible("irrigation"):
            try:
                steps.remove("i")
            except:
                pass

        if not self.__tractor.if_operation_possible("fertilizer"):
            try:
                steps.remove("f")
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
                    # todo optimize
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

        if not steps:
            print(
                "T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(
                    self.__tractor.get_index_y()) + "\tPusta lista")

            if last_step == "L":
                steps.add("R")
            elif last_step == "R":
                steps.add("L")
            elif last_step == "U":
                steps.add("D")
            elif last_step == "D":
                steps.add("U")

        new_steps = sorted(list(steps), key=lambda x: (not x.islower(), x))
        print("T posX: " + str(self.__tractor.get_index_x()) + " posY: " + str(self.__tractor.get_index_y()), end="\t")
        print("New possible steps" + str(new_steps))
        return new_steps

    def __update_map(self, step):
        print(str(self.counter) + ". Movement: " + step)
        self.counter += 1

        if step == "L":
            self.__tractor.move_left()
        elif step == "R":
            self.__tractor.move_right()
        elif step == "U":
            self.__tractor.move_up()
        elif step == "D":
            self.__tractor.move_down()

        if step == "i" or step == "f":
            self.__engine.do_things(self.__map, self.__tractor)
        if step == "h":
            self.__engine.harvest_plants(self.__map, self.__tractor)
        if step == "e":
            # for obj in self.__solid_sprite_group:
            #     if isinstance(obj, Barn):
            #         print(obj.get_rect())

            self.set_plant_score(
                self.__engine.deliver_plants(self.__plant_score, self.__tractor)
            )

        if step == "w" or step == "b":
            self.__engine.refill_tractor(self.__tractor)
            self.__engine.refill_tractor(self.__tractor)

    def update(self, step):
        if (pygame.time.get_ticks() - self.__start_time) / 2 > 1:
            self.__start_time = pygame.time.get_ticks()
            game_map = self.__map
            for fields in game_map:
                for field in fields:
                    for entity in field:
                        if isinstance(entity, AbstractHarvestablePlants):
                            entity.grow()
                            entity.handle_warnings(True)

        return self.__update_map(step)

    def timer(self, a, b):
        while True:
            if self.__engine.get_pause_flag():
                time.sleep(2)
                self.__engine.set_pause_flag(False)

    def set_plant_score(self, plant_score):
        self.__plant_score = plant_score
