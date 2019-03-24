import pygame

from entities.Ground.AbstractEntities import AbstractEntities


class AbstractHarvestable(AbstractEntities):
    def __init__(self, name, image, x, y):
        self.__default_image = image

        super().__init__(name, image, x, y)

        self.__grow_stage = 0
        self.__stats = {}

        self.__init_stats()

    def __init_stats(self):
        water_warning_image = pygame.image.load("resources/sprites/water_warning.png")
        fertilizer_warning_image = pygame.image.load("resources/sprites/fertilizer_warning.png")

        fertilizer = {
            "level": 100,
            "warning_images": fertilizer_warning_image,
            "warning_level": 90,
            "warning": False,
            "rate": 10
        }

        irrigation = {
            "level": 100,
            "warning_images": water_warning_image,
            "warning_level": 90,
            "warning": False,
            "rate": 10
        }

        self.__stats = {
            "irrigation": irrigation,
            "fertilizer": fertilizer
        }

    def get_grow_stage(self):
        return self.__grow_stage

    def update(self, *args):
        self.handle_warnings()

    def grow(self):
        for stat in self.__stats.values():
            if stat["level"] > 0:
                stat["level"] -= stat["rate"]
                if stat["level"] <= 0:
                    stat["level"] = 0

        self.__grow_stage += 1

    def handle_warnings(self):
        self.__check_stats_levels()
        self.__draw_warning()

    def __check_stats_levels(self):
        for stat in self.__stats.values():
            if stat["level"] <= stat["warning_level"]:
                stat["warning"] = True
            else:
                stat["warning"] = False

    def __draw_warning(self):
        self.image = self.__default_image

        counter = 0
        for stat in self.__stats.values():
            if stat["warning"]:
                self.image.blit(stat["warning_images"], (-20 * counter, 0))
            counter += 1

    def get_ground_stats_dict(self):
        return self.__stats

    def take_care(self, stat, capacity):
        self.__stats.get(stat)["level"] += capacity

    def if_operation_possible(self, stat, capacity):
        return True if ((self.__stats.get(stat)["level"] + capacity) <= 100) else False
