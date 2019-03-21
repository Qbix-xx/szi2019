import pygame

from entities.Ground.AbstractHarvestable import AbstractHarvestable


class Plant(AbstractHarvestable):

    def __init__(self, x, y):
        self.__sheet = pygame.image.load("resources/sprites/plant_spritesheet.png").convert_alpha()
        self.image = self.__sheet.subsurface(pygame.Rect(0, 0, 32, 32))
        self.rect = self.image.get_rect()

        super().__init__("Plant", self.image, x, y)

    def update(self, *args):
        super().update()
        if self.get_grow_stage() >= 3:
            self.image = self.__sheet.subsurface(pygame.Rect(32, 0, 32, 32))
            if self.get_grow_stage() >= 6:
                self.image = self.__sheet.subsurface(pygame.Rect(64, 0, 32, 32))
