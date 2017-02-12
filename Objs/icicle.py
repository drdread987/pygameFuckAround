import pygame
import spritesheet
import tools
from Objs import basic_objects


class Icicle(basic_objects.BasicOther):

    def __init__(self, x, y, direction, intelligence):

        super().__init__(x, y)

        self.function = "MISSILE"
        self.depth = 500
        self.height = 64
        self.width = 64
        self.gravity = False

        self.max_speed = 10
        self.current_speed = self.max_speed

        if direction == "RIGHT":
            self.direction = 1
        elif direction == "LEFT":
            self.direction = -1

        self.ss = spritesheet.Spritesheet('images/icicle_0.png')
        img_locs = []
        for x in range(0, 7):
            img_locs.append((x * 64, 0, 64, 64))
        self.images_left = self.ss.images_at(img_locs, colorkey=(0, 0, 0))
        img_locs = []
        for x in range(0, 7):
            img_locs.append((x * 64, 4 * 64, 64, 64))
        self.images_right = self.ss.images_at(img_locs, colorkey=(0, 0, 0))
        self.image_key = 0
        self.image_grab()

        self.image_delay = 1
        self.image_delay_max = 1

        self.max_damage = 1 * intelligence
        self.current_damage = self.max_damage

    def step(self, obj_list):

        super().step(obj_list)

        self.x += self.direction * self.current_speed

        self.image_delay -= 1
        if self.image_delay == 0:
            self.image_delay = self.image_delay_max
            self.image_key += 1
            if self.image_key > len(self.images_right) - 1:
                self.image_key = 0
            if self.direction == 1:
                self.image = self.images_right[self.image_key]
            else:
                self.image = self.images_left[self.image_key]

        units = obj_list.get_unit_list()
        for unit in units:
            if not unit[1].friendly:
                f = unit[1]
                if tools.box_collide(self.x, self.y, self.width, self.height, f.x, f.y, f.width, f.height):
                    unit[1].current_health -= self.current_damage
                    obj_list.kill_other(oid=self.id)

        if self.x < 0 or self.x > 800:
            obj_list.kill_other(oid=self.id)

    def image_grab(self):

        if self.direction == 1:
            self.image = self.images_right[self.image_key]
        else:
            self.image = self.images_left[self.image_key]

