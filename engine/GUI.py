from entities.Ground.AbstractHarvestablePlants import AbstractHarvestablePlants
import pygame


class GUI:
    pygame.init()
    __text_header_font = pygame.font.SysFont('showcardgothic', 30)
    __interface_colour = (0, 0, 0)
    __stats_font = pygame.font.SysFont('unispacebold', 20)
    __hScreen = None
    __current_map_color = (220, 20, 60)
    __selected_map_color = (255, 215, 0)
    __map_size = 0

    @staticmethod
    def set_hScreen(hScreen):
        GUI.__hScreen = hScreen

    @staticmethod
    def set_map_size(map_size):
        GUI.__map_size = map_size

    @staticmethod
    def render_text_header_surface(font, colour, string_name, position_x, position_y, hScreen):
        name_surface = font.render(
            string_name,
            True,
            colour
        )
        hScreen.blit(name_surface, (position_x * 33, position_y * 33))

    @staticmethod
    def render_stats_surface(dict, font, colour, position_x, position_y, hScreen):
        iterator_over_stat_dict_key = 0

        for stat in dict.keys():
            stats_surface = font.render(
                str(stat) + ": "
                + str(dict.get(stat)),
                True,
                colour
            )

            hScreen.blit(stats_surface, (position_x * 33, position_y * 33 + iterator_over_stat_dict_key * 33))
            iterator_over_stat_dict_key += 1

    @staticmethod
    def render_ground_stats_interface(field):

        GUI.render_text_header_surface(
            GUI.__text_header_font,
            GUI.__interface_colour,
            field[len(field) - 1].get_name(),
            GUI.__map_size + 3, 1,
            GUI.__hScreen
        )

        if isinstance(field[len(field) - 1], AbstractHarvestablePlants):
            temp_stats = field[len(field) - 1].get_stats()
            plant_stage = field[len(field) - 1].get_grow_stage()

            dict_to_display = {
                "Watered":      temp_stats["irrigation"]["done"],
                "Fertilized":   temp_stats["fertilizer"]["done"],
                "Growth stage": plant_stage + 1,
                "irrigation":   temp_stats["irrigation"]["level"],
                "fertilizer":   temp_stats["fertilizer"]["level"]
            }

            GUI.render_stats_surface(
                dict_to_display,
                GUI.__stats_font,
                GUI.__interface_colour,
                GUI.__map_size + 3, 2,
                GUI.__hScreen
            )

    @staticmethod
    def render_inventory_interface(plant, plants_score):
        GUI.render_text_header_surface(
            GUI.__text_header_font,
            GUI.__interface_colour,
            "Inventory",
            10, GUI.__map_size + 2,
            GUI.__hScreen
        )

        GUI.render_text_header_surface(
            GUI.__stats_font,
            GUI.__interface_colour,
            "Plants held: " + str(plant) + "/" + str(plants_score),
            10, GUI.__map_size + 3,
            GUI.__hScreen
        )

        GUI.render_text_header_surface(
            GUI.__stats_font,
            GUI.__interface_colour,
            "Plants delivered: " + str(plants_score),
            10, GUI.__map_size + 4,
            GUI.__hScreen

        )

    @staticmethod
    def render_map_list(map_manager):
        GUI.render_text_header_surface(
            GUI.__stats_font,
            GUI.__interface_colour,
            "Map list",
            GUI.__map_size + 3, 10,
            GUI.__hScreen
        )

        y_pos = 10
        map_list = map_manager.get_map_list()
        for map_name in map_list:
            y_pos = y_pos + 1
            if map_name == map_manager.get_map_name():
                map_list_color = GUI.__current_map_color
            elif map_name == map_list[map_manager.get_map_idx()]:
                map_list_color = GUI.__selected_map_color
            else:
                map_list_color = GUI.__interface_colour

            GUI.render_text_header_surface(
                GUI.__stats_font,
                map_list_color,
                map_name,
                GUI.__map_size + 3, y_pos,
                GUI.__hScreen

            )

    @staticmethod
    def render_tractor_stats_interface(tractor_stats):

        dict_to_display = {
            "irrigation": tractor_stats["irrigation"]["level"],
            "fertilizer": tractor_stats["fertilizer"]["level"]
        }

        GUI.render_stats_surface(
            dict_to_display,
            GUI.__stats_font,
            GUI.__interface_colour,
            1, GUI.__map_size + 3,
            GUI.__hScreen
        )

        GUI.render_text_header_surface(
            GUI.__text_header_font,
            GUI.__interface_colour,
            "Tractor Storage",
            1, GUI.__map_size + 2,
            GUI.__hScreen
        )

    @staticmethod
    def render_interface(field, tractor_stats, plant, plants_score, map_manager):
        # grey background
        GUI.__hScreen.fill([100, 100, 100])

        # black background beneath map grid to make lines more visible
        pygame.draw.rect(GUI.__hScreen, [0, 0, 0], (30, 30, 33 * GUI.__map_size + 3, 33 * GUI.__map_size + 3))
        GUI.render_ground_stats_interface(field)
        GUI.render_tractor_stats_interface(tractor_stats)
        GUI.render_inventory_interface(plant, plants_score)
        GUI.render_map_list(map_manager)
