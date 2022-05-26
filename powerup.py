import pygame as pg


class Powerup:
    def __init__(self):

        self.x = self.position.x
        self.y = self.position.y
        self.width = 10
        self.height = 10

    def draw(self, screen):
        pg.draw.rect(
            screen,
            (255, 255, 255),
            [self.position.x, self.position.y, self.width, self.height])