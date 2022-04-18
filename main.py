import pygame
import pygame as pg


class Game:
    clock = pg.time.Clock()
    run = True
    game_over = False

    @staticmethod
    def run():
        pg.display.set_caption('Asteroids')
        while Game.run:
            Game.clock.tick(60)
            if not Game.game_over:
                pass
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.run = False
        pg.quit()

    @staticmethod
    def draw():
        pass


# On start
Game.run()

