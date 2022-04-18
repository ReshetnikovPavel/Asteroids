import pygame
import pygame as pg


class Game:
    clock = pg.time.Clock()
    run = True
    game_over = False
    screen_width = 800
    screen_height = 800
    screen = pg.display.set_mode((screen_width, screen_height))

    @staticmethod
    def run():
        pg.display.set_caption('Asteroids')
        while Game.run:
            Game.clock.tick(60)
            if not Game.game_over:
                Game.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.run = False
        pg.quit()

    @staticmethod
    def draw():
        Game.screen.fill((255, 255, 255))


# On start
Game.run()

