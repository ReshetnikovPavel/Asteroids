import random
import pygame.math as m
import pygame as pg
import vectorRandom

import collision
from bullet import Bullet


class Bonus:
    def __init__(self, game, spawn_point, direction, velocity):
        self.bonus_type = random.choice(["life"])
        self.texture = Bonus.type_to_texture(game, self.bonus_type)
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.spawn_point = spawn_point
        x, y = self.spawn_point
        self.position = m.Vector2(x, y)
        self.direction = direction
        self.velocity = m.Vector2(self.direction.x,
                                  self.direction.y)

    def move(self, game):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def draw(self, window):
        window.blit(self.texture, self.position)

    @staticmethod
    def type_to_texture(game, bonus_type):
        textures = game.textures
        if bonus_type == "life":
            return textures.life_bonus
        elif bonus_type == "shield":
            return textures.shield_bonus
        elif bonus_type == "score":
            return textures.score_bonus
