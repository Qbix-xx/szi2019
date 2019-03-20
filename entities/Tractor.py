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

        self.__irrigate_level_in_storage = 30
        self.__irrigate_rate = 10

        self.__fertilize_level_in_storage = 100
        self.__fertilize_rate = 10

        self.storage_stats_decline_rates = {
            "irrigation": self.__irrigate_rate,
            "fertilizer": self.__fertilize_rate
        }

        self.storage_stats = {
            "irrigation": self.__irrigate_level_in_storage,
            "fertilizer": self.__fertilize_level_in_storage
        }

    def get_index_x(self):
        return self.__index_x

    def get_index_y(self):
        return self.__index_y

    def get_irrigate_rate(self):
        return self.__irrigate_rate

    def get_fertilize_rate(self):
        return self.__fertilize_rate

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
                       and (self.rect.y + step_y <= 33 * self.__map_size) \
            else False

    def operation(self, stat):
        self.storage_stats[stat] -= self.storage_stats_decline_rates[stat]

    def if_operation_posible(self, stat):
        return True if self.storage_stats[stat] - self.storage_stats_decline_rates[stat] >= 0 else False
