import os

from entities.Ground.Grass import Grass
from entities.Ground.Plant import Plant
from entities.Ground.Road import Road
from entities.Ground.Tree import Tree
from entities.Tractor import Tractor
from entities.Barn import Barn

from entities.WaterContainer import WaterContainer


class MapManager:
    def __init__(self):
        self.__map_idx = 0
        self.__maps_path = os.path.join("resources", "map_layouts")
        self.__map_name = None
        self.__map_size = None
        self.__map_layout = None
        self.__map_list = []
        self.__game_map = None
        self.prepare_map_list()

    def load_map(self, map_name):
        with open(os.path.join(self.__maps_path, map_name)) as f:
            self.__map_layout = list(line.replace('\n', '').split(" ") for line in f)
        self.__map_name = map_name
        self.__map_size = len(self.__map_layout)

        idx = -1
        for game_map in self.__map_list:
            idx = idx + 1
            if game_map == self.__map_name:
                break

        self.__game_map = [[[]] * self.__map_size for _ in range(self.__map_size)]
        self.__map_idx = idx

    def get_map_name(self):
        return self.__map_name

    def get_map_size(self):
        return self.__map_size

    def get_map_layout(self):
        return self.__map_layout

    def decrease_map_idx(self):
        self.__map_idx -= 1

        if self.__map_idx < 0:
            self.__map_idx = len(self.__map_list) - 1

    def increase_map_idx(self):
        self.__map_idx += 1

        if self.__map_idx >= len(self.__map_list):
            self.__map_idx = 0

    def set_map_idx(self, map_idx):
        self.__map_idx = map_idx

    def get_map_idx(self):
        return self.__map_idx

    def prepare_map_list(self):
        maps = []
        for (dir_path, dir_names, file_name) in os.walk(self.__maps_path):
            maps.extend(file_name)
            break
        self.__map_list = sorted(maps)

    def get_map_list(self):
        return self.__map_list

    def get_map_layout_name_with_selected_idx(self):
        return self.__map_list[self.__map_idx]

    def create_map_from_layout(self,
                               tractor: Tractor,
                               solid_sprite_group,
                               plants_sprite_group,
                               water_containers_list,
                               barns_list):
        for i in range(self.__map_size):
            for j in range(self.__map_size):

                self.__game_map[i][j] = []
                self.__game_map[i][j].append(Grass(i * 32 + i + 32, j * 32 + j + 32))

                if self.__map_layout[i][j] == "1":
                    self.__game_map[i][j].append(Road(i * 32 + i + 32, j * 32 + j + 32))

                elif self.__map_layout[i][j] == "2":
                    tractor.set_rect_by_index((i, j))

                elif self.__map_layout[i][j] == "3":
                    plant = Plant(i * 32 + i + 32, j * 32 + j + 32)
                    self.__game_map[i][j].append(plant)
                    plants_sprite_group.add(plant)

                elif self.__map_layout[i][j] == "4":
                    tree = Tree(i * 32 + i + 32, j * 32 + j + 32)
                    self.__game_map[i][j].append(tree)
                    solid_sprite_group.add(tree)

                elif self.__map_layout[i][j] == "5":
                    barn = Barn(i * 32 + i + 32, j * 32 + j + 32)
                    barns_list.append(barn)
                    self.__game_map[i][j].append(barn)
                    solid_sprite_group.add(barn)

                elif self.__map_layout[i][j] == "6":
                    water_container = WaterContainer(i * 32 + i + 32, j * 32 + j + 32)
                    water_containers_list.append(water_container)
                    self.__game_map[i][j].append(water_container)
                    solid_sprite_group.add(water_container)

        return self.__game_map
