import pygame
from entities.Tractor import Tractor


def collision_detection(sprite, solid_sprite_group: pygame.sprite.Group):
    flag = False

    for solid_object in solid_sprite_group:
        if solid_object.is_collided_with(sprite):
            flag = True
            break

    return flag


def update_tractor_position(movement_step, tractor: Tractor):
        print("Movement: " + str(movement_step))

        if movement_step == "L":
            tractor.move_left()
        elif movement_step == "R":
            tractor.move_right()
        elif movement_step == "U":
            tractor.move_up()
        elif movement_step == "D":
            tractor.move_down()
