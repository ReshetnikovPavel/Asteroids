import unittest
from level_info import LevelInfo


class TestLevelInfo(unittest.TestCase):
    class GameForTest:
        def __init__(self):
            self.is_audio_on = False
            self.score = 0

    def setUp(self):
        self.game = self.GameForTest()
        self.level_info = LevelInfo(1, 1, 0, 11, 11, 1, 15, self.game)

    def testSameLevel(self):
        self.level_info.check_next_level(0)
        self.assertEqual(1, self.level_info.level_count)
        self.assertEqual(1, self.level_info.ticks_to_next_level)
        self.assertEqual(0, self.level_info.level_start_tick)
        self.assertEqual(11, self.level_info.saucer_timing)
        self.assertEqual(11, self.level_info.asteroids_timing)
        self.assertEqual(1, self.level_info.asteroid_speed_coefficient)
        self.assertEqual(15, self.level_info.saucer_fire_timing)
        self.assertEqual(0, self.game.score)

    def testNextLevel(self):
        self.level_info.check_next_level(2)
        self.assertEqual(2, self.level_info.level_count)
        self.assertEqual(1.5, self.level_info.ticks_to_next_level)
        self.assertEqual(2, self.level_info.level_start_tick)
        self.assertEqual(9.0, self.level_info.saucer_timing)
        self.assertEqual(9.0, self.level_info.asteroids_timing)
        self.assertEqual(1.1, self.level_info.asteroid_speed_coefficient)
        self.assertEqual(10, self.level_info.saucer_fire_timing)
        self.assertEqual(10, self.game.score)


if __name__ == '__main__':
    unittest.main()