import math

from Assets import Textures
import pygame as pg


class Player:
    def __init__(self, screen_width, screen_height):
        textures = Textures()
        self.texture = textures.player
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.position = pg.Vector2(screen_width // 2, screen_height // 2)
        self.angle = 0
        self.rotated_surface = pg.transform.rotate(self.texture, self.angle)
        self.rotated_rectangle = self.rotated_surface.get_rect()
        self.rotated_rectangle.center = self.position
        self.direction = pg.Vector2(
            math.cos(math.radians(self.angle + 90)),
            -math.sin(math.radians(self.angle + 90)))
        self.head = pg.Vector2(
            self.position.x + self.direction.x * self.width // 2,
            self.position.y + self.direction.y * self.height // 2)

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rotated_rectangle)

    def turn_left(self):
        self.angle += 5
        self.update()

    def turn_right(self):
        self.angle -= 5
        self.update()

    def update(self):
        self.rotated_surface = pg.transform.rotate(self.texture, self.angle)
        self.rotated_rectangle = self.rotated_surface.get_rect()
        self.rotated_rectangle.center = self.position
        self.direction = pg.Vector2(
            math.cos(math.radians(self.angle + 90)),
            -math.sin(math.radians(self.angle + 90)))
        self.head = pg.Vector2(
            self.position.x + self.direction.x * self.width // 2,
            self.position.y + self.direction.y * self.height // 2)

    def move_forward(self):
        self.position += self.direction * 6
        self.update()
