import saucer
from main import Game
from asteroid import Asteroid
from bullet import Bullet
from bonus import Bonus
from player import Player
import pygame.math as m
import unittest
import copy
import pygame as pg


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def testGetDestinationForTextHeader(self):
        self.game.screen_width = 1000
        self.game.screen_height = 700
        width = 100
        height = 80
        offset_height = 10
        res_width, res_height = self.game._get_destination_for_text_header(
            width, height, offset_height)
        self.assertEqual(res_width, 450)
        self.assertEqual(res_height, 320)

    def testGetDestinationForNextTextEntry(self):
        self.game.screen_width = 1000
        self.game.screen_height = 700
        width = 100
        height = 80
        i = 3
        horizontal_spacing = 10
        vertical_spacing = 20
        res_width, res_height = self.game._get_destination_for_text_next_entry(
            width, height, i, horizontal_spacing, vertical_spacing)
        self.assertEqual(res_width, 460)
        self.assertEqual(res_height, 400)

    def testStartGame(self):
        game = Game()
        self.assertEqual(True, game.game_over)
        self.assertEqual(game.draw_main_menu, game.draw)
        self.assertEqual(game.handle_menu_events, game.handle_events)
        game.start_game()
        self.assertEqual(False, game.game_over)
        self.assertEqual(game.draw_game, game.draw)
        self.assertEqual(game.handle_game_events, game.handle_events)

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

    def testInRun(self):
        game = Game()
        init_count = game.count
        game.game_over = False
        game.draw = game.draw_game
        game.handle_events = game.handle_game_events
        game.in_run()

        self.assertGreater(game.count, init_count)
        game.count = game.level_info.asteroids_timing - 1
        game.in_run()
        self.assertTrue(len(game.asteroids) > 0)

        game.count = game.level_info.saucer_timing - 1
        game.in_run()
        self.assertTrue(len(game.saucers) > 0)

        game.player.lives = 0
        game.in_run()
        self.assertTrue(self.game.game_over)

    def testDrawGame(self):
        s = saucer.Saucer(self.game)
        self.game.saucers.append(s)
        self.game.asteroids.append(Asteroid(self.game, 1))
        self.game.player.bullets.append(Bullet(self.game.player))
        s.bullets.append(Bullet(s))
        self.game.draw_game()
        self.assertEqual(self.game.elements_drawn, 5)

    def testDrawScoreTable(self):
        self.game.draw_score_table()
        self.assertTrue(self.game.score_entries_drawn > 0)

    def test_init(self):
        self.game.__init__()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
