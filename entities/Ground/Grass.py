import pygame

# from entities.Ground.AbstractHarvestable import AbstractHarvestable
from entities.Ground.AbstractEntities import AbstractEntities


class Grass(AbstractEntities):

    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/grass2.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        super().__init__("Grass", self.image, x, y)

