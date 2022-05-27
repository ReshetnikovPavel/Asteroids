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

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rotated_rectangle)

    def turn_left(self):
        self.angle += 5

    def turn_right(self):
        self.angle -= 5

    def update(self, game):
        self.update_geometry()
        self.check_invincibility(game)

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
        if self.is_invincible:
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
        if self.is_invincible:
            return
        if collision.check_player_triangular_collision(self, bullet):
            if game.is_audio_on:
                pg.mixer.Sound.play(game.audio.explodes[2])
            self.lives -= 1
            self.die(game)

    def die(self, game):
        self.reset(game)
        self.latest_death_frame = game.count

    def check_invincibility(self, game):
        frames_since_death = game.count - self.latest_death_frame
        if frames_since_death < self.invincibility_frames:
            self.is_invincible = True
            if frames_since_death % 2:
                self.switch_texture(game)
        else:
            self.is_invincible = False
            self.texture = game.textures.player

    def switch_texture(self, game):
        if self.texture == game.textures.player:
            self.texture = game.textures.player_no_texture
        else:
            self.texture = game.textures.player

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
