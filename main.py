import pygame as pg
import random

from bullet import Bullet
from player import Player

from asteroid import Asteroid

screen_width = 800
screen_height = 800


class Game:
    clock = pg.time.Clock()
    asteroids = []
    count = 0
    is_run = True
    game_over = False
    screen = pg.display.set_mode((screen_width, screen_height))
    player = Player(screen_width, screen_height)
    player_bullets = []

    @staticmethod
    def run():
        pg.display.set_caption('Asteroids')
        while Game.is_run:
            Game.clock.tick(60)
            Game.count += 1
            if not Game.game_over:
                Game.control_player()
                Game.move_bullets()
                if Game.count % 50 == 0:
                    random_number = random.choice([1, 1, 1, 2, 2, 3])
                    Game.asteroids.append(
                        Asteroid(random_number, screen_width, screen_height))
                Game.draw()

                Game.move_asteroids()
            Game.handle_events()

        pg.quit()

    @staticmethod
    def draw():
        Game.screen.fill((0, 0, 0))
        Game.player.draw(Game.screen)
        for asteroid in Game.asteroids:
            asteroid.draw(Game.screen)
        for bullet in Game.player_bullets:
            bullet.draw(Game.screen)
        pg.display.update()

    @staticmethod
    def move_asteroids():
        for asteroid in Game.asteroids:
            asteroid.x += asteroid.velocity.x
            asteroid.y += asteroid.velocity.y

    @staticmethod
    def move_bullets():
        for bullet in Game.player_bullets:
            bullet.move()
            if bullet.is_off_screen(screen_width, screen_height):
                Game.player_bullets.pop(Game.player_bullets.index(bullet))

    @staticmethod
    def control_player():
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            Game.player.turn_left()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            Game.player.turn_right()
        if keys[pg.K_UP] or keys[pg.K_w]:
            Game.player.move_forward()

    @staticmethod
    def handle_events():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Game.run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not Game.game_over:
                        Game.player_bullets.append(Bullet(Game.player))


# On start
Game.run()
