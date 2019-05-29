import os


class MapManager:
    def __init__(self, maps_path, default_map):
        self.maps_path = maps_path
        self.default_map_name = default_map
        self.__current_map_name = None
        self.__current_map_size = None
        self.__current_map_layout = None
        self.__map_list = []
        self.prepare_map_list()

    def load_map(self, map_name):
        if map_name == "default":
            map_name = self.default_map_name
        with open(os.path.join(self.maps_path, map_name)) as f:
            self.__current_map_layout = list(line.replace('\n', '').split(" ") for line in f)
        self.__current_map_name = map_name
        self.__current_map_size = len(self.__current_map_layout)

    def get_map_name(self):
        return self.__current_map_name

    def get_map_size(self):
        return self.__current_map_size

    def get_map_layout(self):
        return self.__current_map_layout

    def get_map_idx(self):
        idx = -1
        for map in self.map_list:
            idx = idx + 1
            if map == self.__current_map_name:
                break
        return idx

    def prepare_map_list(self):
        maps = []
        for (dirpath, dirnames, filenames) in os.walk(self.maps_path):
            maps.extend(filenames)
            break
        self.map_list = sorted(maps)

    def get_map_list(self):
        return self.map_list

    def get_map_layout_name_with_idx(self, idx):
        return self.map_list[idx]