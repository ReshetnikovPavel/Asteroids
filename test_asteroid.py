import copy
import unittest
import Assets
import asteroid
import bullet
import player
from level_info import LevelInfo
import pygame as pg


class TestBullet(unittest.TestCase):
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
            self.level_info = LevelInfo(1, 1, 1, 1, 1, 1, 1, self)
            self.player = player.Player(self)
            self.score = 0

        def get_score_multiplier(self):
            return 2

    def setUp(self):
        self.game = self.GameForTest(800, 800,
                                     Assets.Textures(), Assets.Audio(),
                                     False, 0)
        self.asteroid = asteroid.Asteroid(self.game, 2)

    def testMove(self):
        init_position = copy.copy(self.asteroid.position)
        self.asteroid.move()
        self.assertNotEqual(init_position, self.asteroid.position)

    def testExplode(self):
        self.asteroid.rank = 1
        self.asteroid.explode(self.game)
        self.assertTrue(len(self.game.asteroids) == 0)
        self.game.asteroids = []

        self.asteroid.rank = 2
        self.asteroid.explode(self.game)
        self.assertTrue(len(self.game.asteroids) != 0)
        self.game.asteroids = []

        self.asteroid.rank = 3
        self.asteroid.explode(self.game)
        self.assertTrue(len(self.game.asteroids) != 0)
        self.game.asteroids = []

        self.asteroid.rank = 1
        self.game.asteroids.append(self.asteroid)
        self.asteroid.explode(self.game)
        self.assertTrue(len(self.game.asteroids) == 0)

    def testRankToTexture(self):
        texture = self.asteroid._rank_to_texture(self.game, 1)
        self.assertTrue(texture in self.game.textures.asteroids_small)
        texture = self.asteroid._rank_to_texture(self.game, 2)
        self.assertTrue(texture in self.game.textures.asteroids_medium)
        texture = self.asteroid._rank_to_texture(self.game, 3)
        self.assertTrue(texture in self.game.textures.asteroids_big)

    def testBulletCollision(self):
        self.game.asteroids.append(self.asteroid)
        b = bullet.Bullet(self.game.player)
        self.game.player.bullets.append(b)
        b.position = self.asteroid.position
        init_score = self.game.score
        self.asteroid.check_bullet_collision(self.game)
        self.assertFalse(self.asteroid in self.game.asteroids)
        self.assertFalse(b in self.game.player.bullets)
        self.assertGreater(self.game.score, init_score)


if __name__ == '__main__':
    unittest.main()
