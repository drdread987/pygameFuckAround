import pygame


class Spritesheet:

    def __init__(self, file_name):

        self.image = pygame.image.load(file_name)

    def image_at(self, rectangle, colorkey):

        rect = pygame.Rect(rectangle)

        image = pygame.Surface(rect.size)
        image.blit(self.image, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def images_at(self, rects, colorkey=None):
        # Loads multiple images, supply a list of coordinates
        return [self.image_at(rect, colorkey) for rect in rects]
