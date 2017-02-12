import pygame
import spritesheet
from Objs import basic_objects
from Objs import icicle


class Player(basic_objects.BasicUnit):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.max_strength = 5
        self.current_strength = self.max_strength

        self.max_dexterity = 5
        self.current_dexterity = self.max_dexterity

        self.max_intelligence = 5
        self.current_intelligence = self.max_intelligence

        self.max_regen = 5
        self.current_regen = self.max_regen

        self.max_fortitude = 5
        self.current_fortitude = self.max_fortitude

        self.max_health = self.current_fortitude * 5
        self.current_health = self.max_health

        self.max_speed = 4
        self.current_speed = self.max_speed

        self.eventer = True
        self.player = True

        self.depth = 1000

        self.direction = "RIGHT"

        self.spell_1_cd_max = 60
        self.spell_1_cd = self.spell_1_cd_max

    def step(self, obj_list):

        super().step(obj_list)

    def handle_events(self, events, obj_list):

        super().handle_events(events, obj_list)

        if self.spell_1_cd < self.spell_1_cd_max:
            self.spell_1_cd += 1

        for event in events:
            print(event)
            if event == 275:
                self.x += self.current_speed
                self.direction = "RIGHT"
            elif event == 276:
                self.x -= self.current_speed
                self.direction = "LEFT"
            elif event == ord(' '):
                self.jump()
            elif event == 274:
                if self.y + self.height < 550 and self.on_ground:
                    self.y += 1
                    self.on_ground = False
            elif event == ord('1') and self.spell_1_cd == self.spell_1_cd_max:
                self.spell_1_cd = 0
                obj_list.new_other(icicle.Icicle(self.x, self.y, self.direction, self.current_intelligence))

    def jump(self):

        if self.on_ground and not self.jumping:

            self.jumping = True
            self.on_ground = False






