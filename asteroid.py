import random
import pygame.math as m
import pygame as pg

import collision
import vectorRandom


class Asteroid:
    def __init__(self, game, rank, spawn_point=None,
                 direction=None):  # rank - размер астероида
        self.rank = rank
        self.texture = self._rank_to_texture(game, rank)
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        if spawn_point is None:
            self.spawn_point = random.choice(
                [(random.randrange(0, game.screen_width - self.width),
                  random.choice(
                      [-1 * self.height - 5, game.screen_height + 5])),
                 (random.choice([-1 * self.width - 5, game.screen_width + 5]),
                  random.randrange(0, game.screen_height - self.height))])
        else:
            self.spawn_point = spawn_point
        x, y = self.spawn_point
        self.position = m.Vector2(x, y)
        if direction is None:
            self.direction = m.Vector2(
                1 if x < game.screen_width // 2 else -1,
                1 if y < game.screen_height // 2 else -1)
        else:
            self.direction = direction
        self.velocity = m.Vector2(self.direction.x * random.randrange(1, 3),
                                  self.direction.y * random.randrange(1, 3))

    @staticmethod
    def _rank_to_texture(game, rank):
        textures = game.textures
        random_number = random.randint(0, 3)
        if rank == 1:
            return textures.asteroids_small[random_number]
        elif rank == 2:
            return textures.asteroids_medium[random_number]
        elif rank == 3:
            return textures.asteroids_big[random_number]

    def draw(self, window):
        window.blit(self.texture, self.position)

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def explode(self, game):
        game.asteroids.remove(self)
        if game.is_audio_on:
            pg.mixer.Sound.play(game.audio.explodes[self.rank-1])
        if self.rank > 1:
            random_vec = vectorRandom.make_rand_vector()
            random_dir = m.Vector2(random_vec[0], random_vec[1])
            game.asteroids.append(Asteroid(
                game,
                self.rank - 1,
                self.position, random_dir))
            game.asteroids.append(Asteroid(
                game,
                self.rank - 1,
                self.position, -random_dir))

    def check_bullet_collision(self, game):
        for bullet in game.player.bullets:
            if collision.check_collision(self, bullet):
                self.explode(game)
                game.score += 1
                game.player.bullets.pop(game.player.bullets.index(bullet))