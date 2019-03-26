import pygame

from entities.AbstractEntities import AbstractEntities


class Tree(AbstractEntities):
    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/tree.png")

        super().__init__("Tree", self.image, x, y)
