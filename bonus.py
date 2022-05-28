import random
import pygame.math as m
import pygame as pg
import vectorRandom

import collision
from bullet import Bullet


class Bonus:
    def __init__(self, game, spawn_point, direction):
        self.activate = random.choice([Bonus.life_bonus, Bonus.score_bonus, Bonus.shield_bonus])
        self.texture = Bonus.type_to_texture(game, self.activate)
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.spawn_point = spawn_point
        x, y = self.spawn_point
        self.position = m.Vector2(x, y)
        self.direction = direction
        self.velocity = m.Vector2(self.direction.x,
                                  self.direction.y)
        self.life = 350

    def move(self, game):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.life -= 1

    def draw(self, game):
        if self.life <= 100 and game.count % 6 > 2:
            return
        game.screen.blit(self.texture, self.position)

    @staticmethod
    def type_to_texture(game, bonus_type):
        textures = game.textures
        if bonus_type == Bonus.life_bonus:
            return textures.life_bonus
        elif bonus_type == Bonus.shield_bonus:
            return textures.shield_bonus
        elif bonus_type == Bonus.score_bonus:
            return textures.score_bonus

    @staticmethod
    def life_bonus(game):
        game.player.lives += 1


    @staticmethod
    def shield_bonus(game):
        game.player.shield = 300

    @staticmethod
    def score_bonus(game):
        game.double_score = 200
