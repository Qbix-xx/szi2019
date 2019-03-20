import pygame

from entities.Ground.AbstractEntities import AbstractEntities


class AbstractHarvestable(AbstractEntities):
    def __init__(self, name, image, x, y):
        super().__init__(name, image, x, y)

        self.__water_warning_image = pygame.image.load("resources/sprites/water_warning.png")
        self.__fertilizer_warning_image = pygame.image.load("resources/sprites/fertilizer_warning.png")

        self.__ground_stats = {
            "irrigation": 100,
            "fertilizer": 100
        }

        self.__ground_decline_rates = {
            "irrigation_rate": 5,
            "fertilizer_rate": 5
        }

        self.__grow_stage = 0

    def get_grow_stage(self):
        return self.__grow_stage

    def grow(self):
        if self.__check_if_stat_can_decline(self.__ground_stats["fertilizer"]):
            self.__ground_stats["fertilizer"] -= self.__ground_decline_rates["fertilizer_rate"]
            if self.__ground_stats["fertilizer"] <= 0:
                self.__ground_stats["fertilizer"] = 0
        if self.__check_if_stat_can_decline(self.__ground_stats["irrigation"]):
            self.__ground_stats["irrigation"] -= self.__ground_decline_rates["irrigation_rate"]
            if self.__ground_stats["irrigation"] <= 0:
                self.__ground_stats["irrigation"] = 0

        self.__grow_stage += 1

    def set_ground_stats(self, irrigation_level, fertilizer_level):
        self.__ground_stats = {
            "irrigation": irrigation_level,
            "fertilizer": fertilizer_level
        }

    def get_ground_stats(self):
        return self.__ground_stats

    def irrigate(self, capacity):
        if self.__check_if_operation_possible(self.__ground_stats["irrigation"], capacity):
            self.__ground_stats["irrigation"] += capacity

    def fertilize(self, capacity):
        if self.__check_if_operation_possible(self.__ground_stats["fertilizer"], capacity):
            self.__ground_stats["fertilizer"] += capacity

    @staticmethod
    def __check_if_operation_possible(level, capacity):
        return True if ((level + capacity) <= 100) else False

    @staticmethod
    def __check_if_stat_can_decline(level):
        return True if level > 0 else False
