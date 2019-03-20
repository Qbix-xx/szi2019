import pygame

from entities.Ground.AbstractHarvestable import AbstractHarvestable


class Grass(AbstractHarvestable):
    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/grass2.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        super().__init__("Grass", self.image, x, y)

        """FROM 0 TO 100% REAL QUICK"""
        # pdk
        self.__irrigation_level = 0  # irrigation level from 0% to 100%
        self.__fertilizer_level = 0  # fertilizer level from 0% to 100%

        self.__stats = {
            "irrigation": self.__irrigation_level,
            "fertilizer": self.__fertilizer_level
        }

    def get_ground_stats(self):
        return self.__stats

    def irrigate(self, capacity):
        if self.check_if_operation_possible(self.__stats["irrigation"], capacity):
            self.__stats["irrigation"] += capacity

    def fertilize(self, capacity):
        if self.check_if_operation_possible(self.__stats["fertilizer"], capacity):
            self.__stats["fertilizer"] += capacity
