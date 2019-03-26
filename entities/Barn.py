import pygame

from entities.AbstractEntities import AbstractEntities


class Barn(AbstractEntities):
    def __init__(self, x, y):
        self.image = pygame.image.load("resources/sprites/barn2.png")

        super().__init__("Barn", self.image, x, y)

        self.refill_hitbox = self.rect.inflate(5, 5)
        self.refill_hitbox.center = self.rect.center

    def get_refill_hitbox(self):
        return self.refill_hitbox
