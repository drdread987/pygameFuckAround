import pygame
from Objs import basic_objects


class Player(basic_objects.BasicUnit):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.current_strength = 5
        self.max_strength = 5

        self.current_dexterity = 5
        self.max_dexterity = 5

        self.current_intelligence = 5
        self.max_intelligence = 5

        self.current_regen = 5
        self.max_regen = 5

        self.current_fortitude = 5
        self.max_fortitude = 5

        self.max_health = self.current_fortitude * 5
        self.current_health = self.max_health

        self.max_speed = 4
        self.current_speed = self.max_speed

        self.eventer = True
        self.player = True

        self.depth = 1000

    def step(self, obj_list):

        super().step(obj_list)

    def handle_events(self, events, obj_list):

        super().handle_events(events, obj_list)

        for event in events:

            if event == ord('d'):
                self.x += self.current_speed
            elif event == ord('a'):
                self.x -= self.current_speed
            elif event == ord(' '):
                self.jump()
            elif event == ord('s'):
                if self.y + self.height < 550 and self.on_ground:
                    self.y += 1
                    self.on_ground = False

    def jump(self):

        if self.on_ground and not self.jumping:

            self.jumping = True
            self.on_ground = False






