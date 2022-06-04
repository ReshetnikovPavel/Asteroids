import unittest
import bullet
import pygame as pg
import pygame.math as pgm
import copy


class TestBullet(unittest.TestCase):
    class PlayerForTest:
        def __init__(self, head, direction, width, height):
            self.head = head
            self.direction = direction
            self.width = width
            self.height = height

    class GameForTest:
        def __init__(self, screen_width, screen_height, is_audio_on, count):
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.is_audio_on = is_audio_on
            self.count = count
            self.asteroids = []
            self.saucers = []
            self.bonuses = []

    def setUp(self):
        player = self.PlayerForTest(
            pgm.Vector2(0, 0),
            pgm.Vector2(10, 10), 1, 1)
        self.bullet = bullet.Bullet(player)
        self.game = self.GameForTest(800, 800, False, 0)

    def testUpdate(self):
        init_position = copy.copy(self.bullet.position)
        init_life = self.bullet.life
        self.bullet.update()
        self.assertNotEqual(self.bullet.position, init_position)
        self.assertLess(self.bullet.life, init_life)

    def testIsOffScreen(self):
        screen_width = 100
        screen_height = 100
        self.bullet.position = pgm.Vector2(200, 200)
        self.assertTrue(
            self.bullet.is_off_screen(screen_width, screen_height))

    def testIsNotOffScreen(self):
        screen_width = 100
        screen_height = 100
        self.bullet.position = pgm.Vector2(0, 0)
        self.assertFalse(
            self.bullet.is_off_screen(screen_width, screen_height))

    def testGetColor(self):
        self.bullet.is_saucer = True
        actual_color = self.bullet._get_color(self.game)
        self.assertEqual(actual_color, (231, 76, 60))
        self.bullet.is_saucer = False
        self.game.double_score = 10
        actual_color = self.bullet._get_color(self.game)
        self.assertEqual(actual_color, (241, 196, 15))
        self.game.double_score = 0
        actual_color = self.bullet._get_color(self.game)
        self.assertEqual(actual_color, (255, 255, 255))


if __name__ == '__main__':
    unittest.main()
