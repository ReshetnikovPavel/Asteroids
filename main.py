import pygame as pg
import random

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
        Game.move_asteroids()

    @staticmethod
    def draw():
        Game.screen.fill((0, 0, 0))
        for asteroid in Game.asteroids:
            asteroid.draw(Game.screen)
        pg.display.update()

    @staticmethod
    def move_asteroids():
        for asteroid in Game.asteroids:
            asteroid.x += asteroid.velocity.x
            asteroid.y += asteroid.velocity.y


# On start
Game.run()


