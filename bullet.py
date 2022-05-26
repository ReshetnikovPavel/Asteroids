import pygame as pg


class Bullet:
    def __init__(self, player, direction=None):
        self.position = player.head
        self.x = self.position.x
        self.y = self.position.y
        self.width = 4
        self.height = 4
        if direction is None:
            self.direction = player.direction
        self.velocity = 10 * direction
        self.life = 100

    def update(self):
        self.position += self.velocity
        self.x = self.position.x
        self.y = self.position.y
        self.life -= 1

    def is_off_screen(self, screen_width, screen_height):
        return self.position.x < -50 or self.position.x > screen_width \
               or self.position.y < -50 or self.position.y > screen_height

    def draw(self, screen):
        pg.draw.rect(
            screen,
            (255, 255, 255),
            [self.position.x, self.position.y, self.width, self.height])
