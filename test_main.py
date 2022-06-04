import unittest
from main import Game
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

    # def testRun(self):
    #    game = Game()
    #    init_count = game.count
    #    game.game_over = False
    #    game.run()
    #    game.is_endless_cycle = False
    #    pg.quit()
#
    #    self.assertGreater(game.count, init_count)
    #    game.count = game.level_info.asteroids_timing
    #    game.run()
    #    pg.quit()

        self.assertTrue(len(game.asteroids) > 0)






if __name__ == '__main__':
    unittest.main()
