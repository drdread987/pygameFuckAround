from Objs import basic_objects
import pygame


class Ground(basic_objects.BasicDoodad):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.function = "WALL"

        self.image = pygame.image.load("images/ground.png")

        self.width = 200
        self.height = 50
        self.gravity = False

