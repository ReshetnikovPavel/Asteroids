import copy
import unittest
import bonus
import Assets
import player
import pygame as pg
import pygame.math as pgm
from level_info import LevelInfo


class TestBonus(unittest.TestCase):
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
            self.double_score = 0

    def setUp(self):
        self.game = self.GameForTest(800, 800,
                                     Assets.Textures(), Assets.Audio(),
                                     False, 0)
        self.bonus = bonus.Bonus(self.game,
                                 pgm.Vector2(0, 0), pgm.Vector2(1, 0))

    def testMove(self):
        init_position = copy.copy(self.bonus.position)
        self.bonus.move(self.game)
        self.assertNotEqual(init_position, self.bonus.position)

    def testLifeBonus(self):
        init_lives = self.game.player.lives
        self.bonus.life_bonus(self.game)
        self.assertGreater(self.game.player.lives, init_lives)

    def testShieldBonus(self):
        init_shield = self.game.player.shield
        self.bonus.shield_bonus(self.game)
        self.assertGreater(self.game.player.shield, init_shield)

    def testDoubleScore(self):
        init_score = self.game.double_score
        self.bonus.score_bonus(self.game)
        self.assertGreater(self.game.double_score, init_score)

    def testTypeToTexture(self):
        texture = self.bonus.type_to_texture(
            self.game, bonus.Bonus.life_bonus)
        self.assertEqual(self.game.textures.life_bonus, texture)
        texture = self.bonus.type_to_texture(
            self.game, bonus.Bonus.shield_bonus)
        self.assertEqual(self.game.textures.shield_bonus, texture)
        texture = self.bonus.type_to_texture(
            self.game, bonus.Bonus.score_bonus)
        self.assertEqual(self.game.textures.score_bonus, texture)


if __name__ == '__main__':
    unittest.main()
