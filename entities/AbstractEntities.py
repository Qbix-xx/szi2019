import abc

import pygame


class AbstractEntities(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image

        self.__name = name

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_surface_image(self):
        return self.image

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def get_name(self):
        return self.__name

    @abc.abstractmethod
    def __init_stats(self):
        pass
