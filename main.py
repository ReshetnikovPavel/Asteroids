import pygame as pg
import random
import collision
import Assets

import pygame.math

from bullet import Bullet
from player import Player

from asteroid import Asteroid

pygame.init()


class Game:
    def __init__(self):
        self.is_audio_on = True
        self.textures = Assets.Textures()
        self.audio = Assets.Audio()
        self.screen_width = 800
        self.screen_height = 800
        self.clock = pg.time.Clock()
        self.asteroids = []
        self.count = 0
        self.is_run = True
        self.game_over = False
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height))
        self.player = Player(self)
        self.score = 0
        self.font = pygame.font.Font(r'Assets/Hyperspace.otf', 36)
        self.scoreText = self.font.render('Score: ' + str(self.score), True,
                                          (255, 255, 255))

    def run(self):
        pg.display.set_caption('Asteroids')
        while self.is_run:
            self.clock.tick(60)
            self.count += 1
            if not self.game_over:
                if self.count % 100 == 0:
                    random_number = random.choice([1, 1, 1, 2, 2, 3])
                    self.asteroids.append(Asteroid(self, random_number))
                self.update()
                self.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
        pg.quit()

    def update(self):
        self.control_player()
        self.player.update()
        self.loop_object(self.player)
        for bullet in self.player.bullets:
            self.loop_object(bullet)
            bullet.update()
            if bullet.life <= 0:
                self.player.bullets.remove(bullet)
        for asteroid in self.asteroids:
            self.loop_object(asteroid)
            asteroid.move()
        self.check_bullet_collision()
        self.handle_events()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.score), True,
                                      (255, 255, 255))
        self.screen.blit(score_text,
                         (self.screen_width - 500,
                          35 + score_text.get_height()))
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for bullet in self.player.bullets:
            bullet.draw(self.screen)
        pg.display.update()

    def control_player(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.turn_left()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.turn_right()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.move_forward(game)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.game_over:
                        self.player.fire(self)

    def loop_object(self, obj):
        if obj.position.x > self.screen_width + obj.height:
            obj.position.x = -obj.height
        elif obj.position.x < -obj.height:
            obj.position.x = self.screen_width + obj.height
        if obj.position.y > self.screen_height + obj.height:
            obj.position.y = -obj.height
        elif obj.position.y < -obj.height:
            obj.position.y = self.screen_height + obj.height

    def check_bullet_collision(self):
        for asteroid in self.asteroids:
            for bullet in self.player.bullets:
                if collision.check_collision(asteroid, bullet):
                    asteroid.explode(game)
                    self.score += 1
                    self.player.bullets.pop(self.player.bullets.index(bullet))


# On start
game = Game()
game.run()
