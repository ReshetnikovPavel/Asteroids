import pygame as pg


class Bullet:
    def __init__(self, player):
        self.position = player.head
        self.width = 4
        self.height = 4
        self.direction = player.direction
        self.velocity = 10 * player.direction

    def move(self):
        self.position += self.velocity

    def is_off_screen(self, screen_width, screen_height):
        return self.position.x < -50 or self.position.x > screen_width \
               or self.position.y < -50 or self.position.y > screen_height


    def draw(self, screen):
        pg.draw.rect(
            screen,
            (255, 255, 255),
            [self.position.x, self.position.y, self.width, self.height])
