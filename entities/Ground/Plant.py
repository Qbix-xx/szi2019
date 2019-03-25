import pygame

from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants


class Plant(AbstractHarvestablePlants):

    def __init__(self, x, y):
        self.__sheet = pygame.image.load("resources/sprites/plant_spritesheet.png").convert_alpha()

        super().__init__("Plant", self.__sheet, x, y)
