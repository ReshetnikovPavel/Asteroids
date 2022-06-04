from main import Game
from asteroid import Asteroid
from bullet import Bullet
from bonus import Bonus
from player import Player
import pygame.math as m
import unittest
import copy


class TestPlayer(unittest.TestCase):
    pass

    def test_loop_object(self):
        game = Game()
        pos1 = m.Vector2(20, 20)
        pos2 = m.Vector2(-1000, 0)
        ast = Asteroid(game, 1, pos1)
        ast.velocity = m.Vector2(0, 0)
        game.loop_object(ast)
        self.assertEqual(pos1, ast.position)
        ast.position = m.Vector2(pos2)
        game.loop_object(ast)
        self.assertNotEqual(pos2, ast.position)

    def test_get_score_multiplier(self):
        game = Game()
        self.assertEqual(1, game.get_score_multiplier())
        game.double_score = 1
        self.assertEqual(2, game.get_score_multiplier())

    def test_end_game(self):
        game = Game()
        self.assertEqual(game.draw_main_menu, game.draw)
        self.assertEqual(game.handle_menu_events, game.handle_events)
        game.end_game()
        self.assertEqual(True, game.game_over)
        self.assertEqual(game.draw_death_screen, game.draw)
        self.assertEqual(game.handle_death_events, game.handle_events)

    def test_update(self):
        game = Game()
        game.start_game()
        asteroid = Asteroid(game, 1, m.Vector2(0, 0))
        asteroid.velocity = m.Vector2(1, 0)
        game.asteroids.append(asteroid)
        player = Player(game)
        bullet = Bullet(player, m.Vector2(1, 0))
        bullet.velocity = m.Vector2(1, 0)
        bonus = Bonus(game, m.Vector2(0, 0), m.Vector2(0, 0))
        bonus.velocity = m.Vector2(1, 0)
        game.bonuses.append(bonus)
        game.update()
        self.assertEqual(m.Vector2(1, 0), asteroid.position)
        self.assertEqual(m.Vector2(400, 380), bullet.position)
        self.assertEqual(m.Vector2(1, 0), bonus.position)


if __name__ == '__main__':
    unittest.main()
    