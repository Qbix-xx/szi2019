import pygame


class AbstractGround(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_surface_image(self):
        return self.image
