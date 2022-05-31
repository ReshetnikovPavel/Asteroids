import copy
import unittest
import Assets
import asteroid
from level_info import LevelInfo


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


if __name__ == '__main__':
    unittest.main()
