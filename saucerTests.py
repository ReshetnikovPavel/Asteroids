import unittest
import pygame.math as pgm
import Assets
import asteroid
import saucer
from level_info import LevelInfo
import copy
import player


class TestSaucer(unittest.TestCase):
    class GameForTest:
        def __init__(self,
                     screen_width, screen_height,
                     textures, audio,
                     is_audio_on, count):
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.textures = textures
            self.audio = audio
            self.is_audio_on = is_audio_on
            self.count = count
            self.asteroids = []
            self.saucers = []
            self.level_info = LevelInfo(1, 1, 1, 1, 1, 1, 1, self)
            self.bonuses = []
            self.player = player.Player(self)

    def setUp(self):
        self.game = self.GameForTest(800, 800,
                                     Assets.Textures(), Assets.Audio(),
                                     False, 0)
        self.saucer = saucer.Saucer(self.game, spawn_point=pgm.Vector2(0, 0))
        self.game.saucers.append(self.saucer)

    def testCheckAsteroidCollisionDied(self):
        a = asteroid.Asteroid(self.game, 2, spawn_point=self.saucer.head)
        self.game.asteroids.append(a)
        self.saucer.check_asteroid_collision(self.game, a)
        self.assertFalse(self.saucer in self.game.saucers)
        self.assertFalse(a in self.game.asteroids)

    def testCheckAsteroidCollisionDidNotDied(self):
        a = asteroid.Asteroid(self.game, 2, spawn_point=pgm.Vector2(100, 100))
        self.game.asteroids.append(a)
        self.saucer.check_asteroid_collision(self.game, a)
        self.assertTrue(self.saucer in self.game.saucers)
        self.assertTrue(a in self.game.asteroids)

    def testExplode(self):
        self.saucer.explode(self.game)
        self.assertFalse(self.saucer in self.game.saucers)
        self.assertTrue(len(self.game.bonuses) > 0)

    def testMove(self):
        init_position = copy.copy(self.saucer.position)
        self.saucer.move(self.game)
        self.assertNotEqual(init_position, self.saucer.position)

    def testFire(self):
        self.saucer.position = pgm.Vector2(0, 0)
        self.game.player.position = pgm.Vector2(10, 0)
        expected_direction = pgm.Vector2(1, 0)
        self.saucer.fire(self.game)
        actual_direction = self.saucer.bullets[0].direction.normalize()
        self.assertEqual(expected_direction, actual_direction)

    def testChangeDirection(self):
        init_direction = copy.copy(self.saucer.direction)
        self.saucer.change_direction()
        self.assertNotEqual(init_direction, self.saucer.direction)

    def testMoveTowardsCenter(self):
        self.game.screen_width = 0
        self.game.screen_height = 0
        self.saucer.position = pgm.Vector2(10, 0)
        self.saucer.move_towards_center(self.game)
        expected_direction = pgm.Vector2(-1, 0)
        actual_direction = self.saucer.direction.normalize()
        self.assertTrue(abs(expected_direction.x - actual_direction.x) < 0.1)
        self.assertTrue(abs(expected_direction.y - actual_direction.y) < 0.1)





if __name__ == '__main__':
    unittest.main()
