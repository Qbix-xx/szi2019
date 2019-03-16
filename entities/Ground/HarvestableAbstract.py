from abc import ABC, abstractmethod

from entities.Ground.AbstractGround import AbstractGround


class HarvestableAbstract(AbstractGround, ABC):
    def __init__(self, name, image, x, y):
        super().__init__(image, x, y)

        self.name = name

    def check_if_operation_possible(self, level, capacity):
        return True if ((level + capacity) <= 100) else False

    @abstractmethod
    def get_ground_stats(self):
        pass
