from abc import ABC

import pygame

from entities.AbstractEntities import AbstractEntities
from entities.AbstractHarvestableInterface import AbstractHarvestableInterface


class AbstractHarvestablePlants(AbstractEntities, AbstractHarvestableInterface, ABC):

    def __init__(self, name, spritesheet, x, y):
        self.__grow_stage_images = {}
        self.__current_clean_image = None
        self.__grow_stage = 0

        self.__init_sprite_sheet(spritesheet)
        super().__init__(name, spritesheet, x, y)
        self.__init_stats()

    def __init_sprite_sheet(self, image):
        for i in range(0, int(image.get_width() / 32)):
            self.__grow_stage_images[i] = image.subsurface(pygame.Rect(i * 32, 0, 32, 32))

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
            "warning_level": 90,
            "warning": False,
            "done": False,
            "rate": 10
        }

        stats = {
            "irrigation": irrigation,
            "fertilizer": fertilizer
        }

        self.set_stats(stats)

    def __reset_stats(self):
        for stat in self.get_stats().values():
            stat["level"] = 100

    def get_grow_stage(self):
        return self.__grow_stage

    def update(self, *args):
        self.__update_stage_image()
        self.__handle_warnings()

    def check_progress(self):
        if self.__grow_stage < 2:
            self.__grow_stage += 1

    def grow(self):
        for stat in self.get_stats().values():
            stat["level"] -= stat["rate"]
            if stat["level"] <= 0:
                stat["level"] = 0

        self.check_progress()

    def is_grown(self):
        max_stage = len(self.__grow_stage_images) - 1
        return True if self.__grow_stage == max_stage else False

    def __update_stage_image(self):
        for stage in self.get_grow_stage_images():
            if self.get_grow_stage() >= stage:
                self.__current_clean_image = self.get_grow_stage_images()[stage].copy()

        self.image = self.__current_clean_image

    def __handle_warnings(self):
        self.__check_stats_levels()
        self.__draw_warning()

    def __check_stats_levels(self):
        for stat in self.get_stats().values():
            if stat["level"] <= stat["warning_level"]:
                stat["warning"] = True
            else:
                stat["warning"] = False

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
        self.__check_stat_level(stat)
        # self.__check_stats_levels()

    def if_operation_possible(self, stat, capacity):
        return True if ((self.get_stats().get(stat)["level"] + capacity) <= 100) else False
