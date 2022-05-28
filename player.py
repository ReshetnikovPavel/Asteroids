import math
import pygame as pg

import collision
from bullet import Bullet


class Player:
    def __init__(self, game):
        self.texture = game.textures.player
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.position = pg.Vector2(game.screen_width // 2,
                                   game.screen_height // 2)
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
        self.velocity = pg.Vector2(0, 0)
        self.acceleration = 0.18
        self.max_speed = 10
        self.bullets = []
        self.lives = 3
        self.invincibility_frames = 100
        self.latest_death_frame = -self.invincibility_frames
        self.is_invincible = False
        self.shield = 0

    def draw(self, game):
        if self.is_invincible and game.count % 6 > 2:
            return
        game.screen.blit(self.rotated_surface, self.rotated_rectangle)

    def turn_left(self):
        self.angle += 5

    def turn_right(self):
        self.angle -= 5

    def update(self, game):
        self.update_texture(game)
        self.update_geometry()
        self.check_invincibility(game)
        if self.shield > 0:
            self.shield -= 1

    def update_texture(self, game):
        if self.shield > 100 or self.shield > 0 and game.count % 6 > 2:
            self.texture = game.textures.shielded_player
        else:
            self.texture = game.textures.player

    def update_geometry(self):
        self.rotated_surface = pg.transform.rotate(self.texture, self.angle)
        self.rotated_rectangle = self.rotated_surface.get_rect()
        self.rotated_rectangle.center = self.position
        self.direction = pg.Vector2(
            math.cos(math.radians(self.angle + 90)),
            -math.sin(math.radians(self.angle + 90)))
        self.head = pg.Vector2(
            self.position.x + self.direction.x * self.width // 2,
            self.position.y + self.direction.y * self.height // 2)
        self.position += self.velocity

    def move_forward(self, game):
        if game.is_audio_on:
            pg.mixer.Sound.play(game.audio.thrust)
        self.velocity += self.direction.normalize() * self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def fire(self, game):
        if game.is_audio_on:
            pg.mixer.Sound.play(game.audio.fire)
        self.bullets.append(Bullet(self))

    def check_asteroid_collision(self, game, asteroid):
        if self.is_invincible or self.shield > 0:
            return
        if collision.check_player_triangular_collision(self, asteroid):
            asteroid.explode(game)
            if not hasattr(asteroid, 'rank'):
                self.lives -= 1
            elif asteroid.rank == 1:
                self.lives -= 0.5
            elif asteroid.rank == 2:
                self.lives -= 1
            elif asteroid.rank == 3:
                self.lives -= 2
            self.die(game)

    def check_bullet_collision(self, game, bullet):
        if self.is_invincible or self.shield > 0:
            return
        if collision.check_player_triangular_collision(self, bullet):
            if game.is_audio_on:
                pg.mixer.Sound.play(game.audio.explodes[2])
            self.lives -= 1
            self.die(game)

    def check_bonus_collision(self, game, bonus):
        if collision.check_player_triangular_collision(self, bonus):
            game.bonuses.remove(bonus)
            bonus.activate(game)
            game.score += 3 * game.get_score_multiplier()
            if game.is_audio_on:
                pg.mixer.Sound.play(game.audio.bonus)

    def die(self, game):
        self.reset(game)
        self.latest_death_frame = game.count

    def check_invincibility(self, game):
        frames_since_death = game.count - self.latest_death_frame
        if frames_since_death < self.invincibility_frames:
            self.is_invincible = True
        else:
            self.is_invincible = False

    def reset(self, game):
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.position = pg.Vector2(game.screen_width // 2,
                                   game.screen_height // 2)
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
        self.velocity = pg.Vector2(0, 0)
