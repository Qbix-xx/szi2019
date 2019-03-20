import pygame

from entities.Ground.AbstractEntities import AbstractEntities


class Tree(AbstractEntities):
    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/tree.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        super().__init__("Tree", self.image, x, y)
