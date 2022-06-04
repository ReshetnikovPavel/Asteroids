import pygame as pg
import copy


class Bullet:
    def __init__(self, player, direction=None, is_saucer=False):
        self.position = copy.copy(player.head)
        self.x = self.position.x
        self.y = self.position.y
        self.width = 4
        self.height = 4
        if direction is None:
            self.direction = player.direction
        else:
            self.direction = direction
        self.velocity = 10 * self.direction
        self.life = 100
        self.is_saucer = is_saucer

    def update(self):
        self.position += self.velocity
        self.x = self.position.x
        self.y = self.position.y
        self.life -= 1

    def is_off_screen(self, screen_width, screen_height):
        return self.position.x < -50 or self.position.x > screen_width \
               or self.position.y < -50 or self.position.y > screen_height

    def draw(self, game):
        pg.draw.rect(
            game.screen,
            self._get_color(game),
            [self.position.x, self.position.y, self.width, self.height])

    def _get_color(self, game):
        if self.is_saucer:
            return 231, 76, 60
        elif game.double_score > 0:
            return 241, 196, 15
        else:
            return 255, 255, 255
