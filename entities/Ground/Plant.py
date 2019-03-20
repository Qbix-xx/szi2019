from abc import ABC

import pygame

from entities.Ground.AbstractHarvestable import AbstractHarvestable


class Plant(AbstractHarvestable, ABC):

    def __init__(self, x, y):
        self.__sheet = pygame.image.load("resources/sprites/plant_spritesheet.png").convert_alpha()
        # self.image = pygame.image.load("resources/sprites/grass.png")
        # self.image = pygame.transform.scale(self.image, (32, 32))
        self.image = self.__sheet.subsurface(pygame.Rect(0, 0, 32, 32))
        self.rect = self.image.get_rect()

        super().__init__("Plant", self.image, x, y)

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
