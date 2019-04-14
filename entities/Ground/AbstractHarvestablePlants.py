from abc import ABC

import pygame

from entities.AbstractEntities import AbstractEntities
from entities.AbstractHarvestableInterface import AbstractHarvestableInterface


class AbstractHarvestablePlants(AbstractEntities, AbstractHarvestableInterface, ABC):

    def __init__(self, name, spritesheet, x, y):
        self.__grow_stage_images = {}
        self.__current_clean_image = None
        self.__grow_stage = 0
        self.__max_grow_stage = 0

        self.__init_sprite_sheet(spritesheet)
        super().__init__(name, spritesheet, x, y)
        self.__init_stats()

    def __init_sprite_sheet(self, image):
        for i in range(0, int(image.get_width() / 32)):
            self.__grow_stage_images[i] = image.subsurface(pygame.Rect(i * 32, 0, 32, 32))

        self.__max_grow_stage = len(self.__grow_stage_images) - 1

    def get_grow_stage_images(self):
        return self.__grow_stage_images

    def __init_stats(self):
        water_warning_image = pygame.image.load("resources/sprites/water_warning.png")
        fertilizer_warning_image = pygame.image.load("resources/sprites/fertilizer_warning.png")

        fertilizer = {
            "level": 100,
            "warning_images": fertilizer_warning_image,
            "warning_level": 80,
            "warning": False,
            "done": False,
            "rate": 10
        }

        irrigation = {
            "level": 100,
            "warning_images": water_warning_image,
            "warning_level": 50,
            "warning": False,
            "done": False,
            "rate": 10
        }

        stats = {
            "irrigation": irrigation,
            "fertilizer": fertilizer
        }

        self.set_stats(stats)

    def get_grow_stage(self):
        return self.__grow_stage

    def update(self, *args):
        self.__update_stage_image()
        self.__handle_warnings()

    def check_progress(self):
        if self.__grow_stage < self.__max_grow_stage:
            self.__grow_stage += 1

    def grow(self):
        if self.get_stats()["irrigation"]["done"] == False:
            stat = self.get_stats()["irrigation"]
            stat["level"] -= stat["rate"]
            if stat["level"] <= 0:
                stat["level"] = 0

            if stat["done"] and self.get_stats()["fertilizer"]["done"]:
                stat = self.get_stats()["fertilizer"]
                stat["level"] -= stat["rate"]
                if stat["level"] <= 0:
                    stat["level"] = 0

        ##dev_end
        # for stat in self.get_stats().values():
        #     stat["level"] -= stat["rate"]
        #     if stat["level"] <= 0:
        #         stat["level"] = 0
        #
        self.check_progress()

    def __grow_first_stage(self):
        a = 1

    def __grow_second_stage(self):
        a = 1

    def is_grown(self):
        return True if self.__grow_stage == self.__max_grow_stage else False

    def __update_stage_image(self):
        for stage in self.get_grow_stage_images():
            if self.get_grow_stage() >= stage:
                self.__current_clean_image = self.get_grow_stage_images()[stage].copy()

        self.image = self.__current_clean_image

    def __handle_warnings(self):
        self.__check_all_stat_level()
        self.__draw_warning()

    def __check_all_stat_level(self):
        for stat in self.get_stats():
            self.__check_stat_level(stat)

    def __check_stat_level(self, stat):
        stat = self.get_stats()[stat]
        if stat["level"] <= stat["warning_level"]:
            stat["warning"] = True
        else:
            stat["warning"] = False

    def __draw_warning(self):

        counter = 0
        for stat in self.get_stats().values():
            if stat["warning"]:
                self.__current_clean_image.blit(stat["warning_images"], (-20 * counter, 20))

            counter += 1

        self.image = self.__current_clean_image

    def take_care(self, stat, capacity):
        self.get_stats().get(stat)["level"] += capacity
        self.get_stats().get(stat)["done"] = True
        self.__check_stat_level(stat)

    def if_operation_possible(self, stat, capacity):
        return True if ((self.get_stats().get(stat)["level"] + capacity) <= 100) and\
                       self.get_stats()[stat]["warning"] else False
