import abc


class AbstractHarvestableInterface:
    def __init__(self):
        self.__stats = {}

    @abc.abstractmethod
    def __init_stat(self):
        pass

    @abc.abstractmethod
    def set_stats(self, stats):
        self.__stats = stats

    @abc.abstractmethod
    def get_stats(self):
        return self.__stats
