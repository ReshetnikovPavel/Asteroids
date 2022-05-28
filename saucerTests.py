import unittest
import player
import Assets
import bullet
import copy
import pygame.math as pgm
import asteroid
import saucer


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

    def setUp(self):
        self.game = self.GameForTest(800, 800,
                                     Assets.Textures(), Assets.Audio(),
                                     False, 0)
        self.saucer = saucer.Saucer(self.game)


    def TestMoveNormal(self):
        pass
if __name__ == '__main__':
    unittest.main()
