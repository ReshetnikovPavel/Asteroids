import unittest
import bullet
import pygame.math as pgm
import copy


class TestBullet(unittest.TestCase):
    class PlayerForTest:
        def __init__(self, head, direction, width, height):
            self.head = head
            self.direction = direction
            self.width = width
            self.height = height

    def setUp(self):
        player = self.PlayerForTest(
            pgm.Vector2(0, 0),
            pgm.Vector2(10, 10), 1, 1)
        self.bullet = bullet.Bullet(player)

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
        self.assertTrue(self.bullet.is_off_screen(screen_width, screen_height))

    def testIsNotOffScreen(self):
        screen_width = 100
        screen_height = 100
        self.bullet.position = pgm.Vector2(0, 0)
        self.assertFalse(self.bullet.is_off_screen(screen_width, screen_height))


if __name__ == '__main__':
    unittest.main()



