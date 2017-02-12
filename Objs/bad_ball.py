import pygame
import tools
import random
from Objs import basic_objects


class BadBall(basic_objects.BasicUnit):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.friendly = False

        self.max_speed = 2
        self.current_speed = self.max_speed

        self.max_health = 10
        self.current_health = self.max_health

        self.depth = 750

        self.image = pygame.image.load('images/bad_ball.png')

        self.found_player = None

        self.max_damage = 1
        self.current_damage = self.max_damage

    def step(self, obj_list):

        super().step(obj_list)

        self.current_speed = random.randint(0, self.max_speed)

        if self.on_ground and not self.jumping:

            self.jumping = True
            self.on_ground = False

        units = obj_list.get_unit_list()
        player = None
        if self.found_player is None:
            for unit in units:
                if unit[1].player:
                    self.found_player = unit[0]
                    player = unit[1]
        else:
            player = obj_list.get_unit(uid=self.found_player)[1]

        if player.x + (player.width / 2) > self.x + (self.width / 2):
            self.x += self.current_speed
        elif player.x + (player.width / 2) < self.x + (self.width / 2):
            self.x -= self.current_speed

        for unit in units:
            if unit[1].friendly:
                f = unit[1]
                if tools.box_collide(self.x, self.y, self.width, self.height, f.x, f.y, f.width, f.height):
                    unit[1].current_health -= self.current_damage

