import pygame as pg
import random

import pygame.math

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
                if Game.count % 50 == 0:
                    random_number = random.choice([1, 1, 1, 2, 2, 3])
                    Game.asteroids.append(Asteroid(random_number, screen_width, screen_height))
                Game.update()
                Game.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.run = False
        pg.quit()

    @staticmethod
    def update():
        Game.control_player()
        Game.update_bullets()
        Game.player.update()
        Game.loop_object(Game.player)
        for bullet in Game.player_bullets:
            Game.loop_object(bullet)
        Game.move_asteroids()
        Game.handle_events()

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
    def update_bullets():
        for bullet in Game.player_bullets:
            bullet.update()
            if bullet.life <= 0:
                Game.player_bullets.remove(bullet)

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

    @staticmethod
    def loop_object(obj):
        if obj.position.x > screen_width + obj.height:
            obj.position.x = -obj.height
        elif obj.position.x < -obj.height:
            obj.position.x = screen_width + obj.height
        if obj.position.y > screen_height + obj.height:
            obj.position.y = -obj.height
        elif obj.position.y < -obj.height:
            obj.position.y = screen_height + obj.height

    @staticmethod
    def explode_asteroid(asteroid):
        Game.asteroids.remove(asteroid)
        if asteroid.rank > 1:
            random_vec = Game.make_rand_vector()
            random_dir = pygame.math.Vector2(random_vec[0], random_vec[1])
            Game.asteroids.append(Asteroid(
                asteroid.rank-1, screen_width, screen_height, (asteroid.x, asteroid.y), random_dir))
            Game.asteroids.append(Asteroid(
                asteroid.rank-1, screen_width, screen_height, (asteroid.x, asteroid.y), -random_dir))

    @staticmethod
    def make_rand_vector():
        vec = [random.gauss(0, 1) for i in range(2)]
        mag = sum(x ** 2 for x in vec) ** .5
        return [x / mag for x in vec]



# On start
Game.run()
