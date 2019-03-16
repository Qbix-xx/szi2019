import pygame

from entities.Ground.HarvestableAbstract import HarvestableAbstract


class Road(HarvestableAbstract):
    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/dirt.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        super().__init__("Road", self.image, x, y)

    def get_ground_stats(self):
        return {}
