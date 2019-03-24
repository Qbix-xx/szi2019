import pygame


class Tractor(pygame.sprite.Sprite):
    def __init__(self, map_size):
        pygame.sprite.Sprite.__init__(self)

        self.__map_size = map_size

        self.__sheet = pygame.image.load("resources/sprites/tractor_spritesheet.png").convert_alpha()
        self.image = self.__sheet.subsurface(pygame.Rect(0, 0, 32, 32))
        self.rect = self.image.get_rect()

        # starting position
        # default is [1,1] in map matrix, upper left corner of map
        self.set_rect(1, 1)

        # position in map matrix
        self.__index_x = int((self.rect.x - 32) / 32)
        self.__index_y = int((self.rect.y - 32) / 32)

        # 1 is needed because of additional lines between grid
        self.__step = 32 + 1

        self.__fertilizer = {
            "level": 100,
            "rate": 10
        }

        self.__irrigation = {
            "level": 100,
            "rate": 10
        }

        self.__stats = {
            "irrigation": self.__irrigation,
            "fertilizer": self.__fertilizer
        }

    def set_storage_stats(self, irrigation_level, fertilizer_level):
        self.__storage_stats = {
            "irrigation": irrigation_level,
            "fertilizer": fertilizer_level
        }

    def set_storage_stats_decline_rates(self, irrigation_level, fertilizer_level):
        self.storage_stats_decline_rates = {
            "irrigation": irrigation_level,
            "fertilizer": fertilizer_level
        }

    def get_ground_stats_dict(self):
        return self.__stats

    def get_ground_stat(self, stat):
        return self.__storage_stats[stat]

    def get_index_x(self):
        return self.__index_x

    def get_index_y(self):
        return self.__index_y

    def set_rect(self, x, y):
        self.rect.x = x * 32
        self.rect.y = y * 32

    def move_right(self):
        self.update_position(self.__step, 0)

    def move_left(self):
        self.update_position(-self.__step, 0)

    def move_down(self):
        self.update_position(0, self.__step)

    def move_up(self):
        self.update_position(0, -self.__step)

    def update_position(self, step_x, step_y):
        if self.__check_if_update_position_possible(step_x, step_y):
            self.rect.x += step_x
            self.__index_x = int((self.rect.x - 32) / 32)

            self.rect.y += step_y
            self.__index_y = int((self.rect.y - 32) / 32)

    def __check_if_update_position_possible(self, step_x, step_y):
        return True if (self.rect.x + step_x >= 32) \
                       and (self.rect.x + step_x <= 33 * self.__map_size) \
                       and (self.rect.y + step_y >= 32) \
                       and (self.rect.y + step_y <= 33 * self.__map_size) else False

    def operation(self, stat):
        self.__stats.get(stat)["level"] -= self.__stats.get(stat)["rate"]

    def if_operation_posible(self, stat):
        return True if self.__stats.get(stat)["level"] - self.__stats.get(stat)["rate"] >= 0 else False
