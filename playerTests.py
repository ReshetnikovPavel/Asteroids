import unittest
import player
import Assets
import bullet
import copy
import pygame.math as pgm
import asteroid
from level_info import LevelInfo


class TestPlayer(unittest.TestCase):
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
        self.player = player.Player(self.game)

    def testTurnLeft(self):
        initial_angle = self.player.angle
        self.player.turn_left()
        self.assertGreater(self.player.angle, initial_angle)

    def testTurnRight(self):
        initial_angle = self.player.angle
        self.player.turn_right()
        self.assertLess(self.player.angle, initial_angle)

    def testFire(self):
        self.player.fire(self.game)
        self.assertTrue(type(self.player.bullets[0]) is bullet.Bullet)

    def testMoveForward(self):
        initial_velocity = copy.copy(self.player.velocity)
        self.player.move_forward(self.game)
        self.assertGreater(self.player.velocity.x, initial_velocity.x)

    def testMoveForwardMaxSpeed(self):
        self.player.velocity = pgm.Vector2(self.player.max_speed, 0)
        self.player.move_forward(self.game)
        self.assertEqual(self.player.velocity.length(), self.player.max_speed)
        self.player.velocity = pgm.Vector2(0, 0)

    def testReset(self):
        init_position = copy.copy(self.player.position)
        init_velocity = copy.copy(self.player.velocity)
        init_angle = copy.copy(self.player.angle)
        init_head = copy.copy(self.player.head)
        self.player.position = pgm.Vector2(5, 5)
        self.player.velocity = pgm.Vector2(5, 5)
        self.player.angle = 5
        self.player.head = pgm.Vector2(6, 6)
        self.player.reset(self.game)
        self.assertEqual(init_position, self.player.position)
        self.assertEqual(init_velocity, self.player.velocity)
        self.assertEqual(init_angle, self.player.angle)
        self.assertEqual(init_head, self.player.head)

    def testCheckInvincibilityIsInvincible(self):
        self.player.latest_death_frame = 0
        self.game.count = self.player.invincibility_frames / 2
        self.player.check_invincibility(self.game)
        self.assertTrue(self.player.is_invincible)
        self.game.count = 0

    def testCheckInvincibilityIsNotInvincible(self):
        self.player.latest_death_frame = 0
        self.game.count = self.player.invincibility_frames * 2
        self.player.check_invincibility(self.game)
        self.assertFalse(self.player.is_invincible)
        self.game.count = 0

    def testCheckAsteroidCollisionDied(self):
        init_lives = self.player.lives
        a = asteroid.Asteroid(self.game, 2, spawn_point=self.player.head)
        self.player.check_asteroid_collision(self.game, a)
        self.assertLess(self.player.lives, init_lives)

    def testCheckAsteroidCollisionDidNotDied(self):
        init_lives = self.player.lives
        a = asteroid.Asteroid(self.game, 2, spawn_point=pgm.Vector2(100, 100))
        self.player.check_asteroid_collision(self.game, a)
        self.assertEqual(self.player.lives, init_lives)

    def testCheckBulletCollisionDied(self):
        init_lives = self.player.lives
        b = bullet.Bullet(self.player)
        b.position = self.player.head - pgm.Vector2(1, 1)
        self.player.check_bullet_collision(self.game, b)
        self.assertLess(self.player.lives, init_lives)

    def testCheckBulletCollisionDidNotDied(self):
        init_lives = self.player.lives
        b = bullet.Bullet(self.player)
        b.position = pgm.Vector2(100, 100)
        self.player.check_bullet_collision(self.game, b)
        self.assertEqual(self.player.lives, init_lives)


if __name__ == '__main__':
    unittest.main()
