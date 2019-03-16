from abc import ABC

import pygame


class AbstractGround(pygame.sprite.Sprite, ABC):
    def __init__(self, name, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image

        self.__name = name

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_surface_image(self):
        return self.image

    def get_name(self):
        return self.__name
