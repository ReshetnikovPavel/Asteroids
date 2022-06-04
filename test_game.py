import copy
import unittest
import Assets
import asteroid
import bullet
import player
from level_info import LevelInfo
import pygame as pg
import copy
import unittest
import bonus
import Assets
import player
import pygame.math as pgm
from level_info import LevelInfo
from score_table import ScoreTable
import unittest
import unittest
import bullet
import copy
import unittest
import collision


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


class TestCollisions(unittest.TestCase):
    class BoxForTest:
        def __init__(self, position, width, height):
            self.position = position
            self.width = width
            self.height = height

    class PlayerForTest:
        def __init__(self, head, direction, width, height):
            self.head = head
            self.direction = direction
            self.width = width
            self.height = height

    def setUp(self):
        self.box = self.BoxForTest(position=pgm.Vector2(0, 0),
                                   width=10,
                                   height=10)
        self.triangle_vertices = [pgm.Vector2(0, 0),
                                  pgm.Vector2(2, 5),
                                  pgm.Vector2(4, 0)]
        self.player = self.PlayerForTest(head=pgm.Vector2(0, 0),
                                         direction=pgm.Vector2(0, 1),
                                         width=10,
                                         height=20)

    def testPointInBoxCollision(self):
        point = pgm.Vector2(5, 5)
        self.assertTrue(collision._is_point_in_box(self.box, point))

    def testPointOutsideBoxCollision(self):
        point = pgm.Vector2(20, 20)
        self.assertFalse(collision._is_point_in_box(self.box, point))

    def testPointOnBorderBoxCollision(self):
        point = pgm.Vector2(10, 10)
        self.assertTrue(collision._is_point_in_box(self.box, point))

    def testPointInsideTriangleCollision(self):
        point = pgm.Vector2(2, 2)
        self.assertTrue(collision._is_point_in_triangle(self.triangle_vertices,
                                                        point))

    def testPointOutsideTriangleCollision(self):
        point = pgm.Vector2(20, 20)
        self.assertFalse(
            collision._is_point_in_triangle(self.triangle_vertices, point))

    def testPointOnBorderTriangleCollision(self):
        point1 = pgm.Vector2(2, 0)
        point2 = pgm.Vector2(1, 2.5)
        self.assertTrue(collision._is_point_in_triangle(self.triangle_vertices,
                                                        point1))
        self.assertTrue(collision._is_point_in_triangle(self.triangle_vertices,
                                                        point2))

    def testTwoBoxesDoCollideCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(-10, -10),
                              width=15,
                              height=15)
        self.assertTrue(collision.check_collision(self.box, box))

    def testTwoBoxesDoNotCollideCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(-10, -10),
                              width=2,
                              height=2)
        self.assertFalse(collision.check_collision(self.box, box))

    def testTwoBoxesCollideOnEdgeCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(10, 0),
                              width=8,
                              height=5)
        self.assertTrue(collision.check_collision(self.box, box))

    def testPlayerTriangleAndBoxDoCollideCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(0, 0),
                              width=8,
                              height=5)
        self.assertTrue(
            collision.check_player_triangular_collision(self.player, box))

    def testPlayerTriangleAndBoxDoNotCollideCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(100, 100),
                              width=8,
                              height=5)
        self.assertFalse(collision.check_player_triangular_collision(
            self.player, box))

import unittest
import pygame as pg
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

import saucer
from main import Game
from asteroid import Asteroid
from bullet import Bullet
from bonus import Bonus
from player import Player
import pygame.math as m
import unittest
import copy
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

    def test_loop_object(self):
        game = Game()
        pos1 = m.Vector2(20, 20)
        pos2 = m.Vector2(-1000, 0)
        ast = Asteroid(game, 1, pos1)
        ast.velocity = m.Vector2(0, 0)
        game.loop_object(ast)
        self.assertEqual(pos1, ast.position)
        ast.position = m.Vector2(pos2)
        game.loop_object(ast)
        self.assertNotEqual(pos2, ast.position)

    def test_get_score_multiplier(self):
        game = Game()
        self.assertEqual(1, game.get_score_multiplier())
        game.double_score = 1
        self.assertEqual(2, game.get_score_multiplier())

    def test_end_game(self):
        game = Game()
        self.assertEqual(game.draw_main_menu, game.draw)
        self.assertEqual(game.handle_menu_events, game.handle_events)
        game.end_game()
        self.assertEqual(True, game.game_over)
        self.assertEqual(game.draw_death_screen, game.draw)
        self.assertEqual(game.handle_death_events, game.handle_events)

    def test_update(self):
        game = Game()
        game.start_game()
        asteroid = Asteroid(game, 1, m.Vector2(0, 0))
        asteroid.velocity = m.Vector2(1, 0)
        game.asteroids.append(asteroid)
        player = Player(game)
        bullet = Bullet(player, m.Vector2(1, 0))
        bullet.velocity = m.Vector2(1, 0)
        bonus = Bonus(game, m.Vector2(0, 0), m.Vector2(0, 0))
        bonus.velocity = m.Vector2(1, 0)
        game.bonuses.append(bonus)
        game.update()
        self.assertEqual(m.Vector2(1, 0), asteroid.position)
        self.assertEqual(m.Vector2(400, 380), bullet.position)
        self.assertEqual(m.Vector2(1, 0), bonus.position)

    def testInRun(self):
        game = Game()
        init_count = game.count
        game.game_over = False
        game.draw = game.draw_game
        game.handle_events = game.handle_game_events
        game.in_run()

        self.assertGreater(game.count, init_count)
        game.count = game.level_info.asteroids_timing - 1
        game.in_run()
        self.assertTrue(len(game.asteroids) > 0)

        game.count = game.level_info.saucer_timing - 1
        game.in_run()
        self.assertTrue(len(game.saucers) > 0)

        game.player.lives = 0
        game.in_run()
        self.assertTrue(self.game.game_over)

    def testDrawGame(self):
        s = saucer.Saucer(self.game)
        self.game.saucers.append(s)
        self.game.asteroids.append(Asteroid(self.game, 1))
        self.game.player.bullets.append(Bullet(self.game.player))
        s.bullets.append(Bullet(s))
        self.game.draw_game()
        self.assertEqual(self.game.elements_drawn, 5)

    def testDrawScoreTable(self):
        self.game.draw_score_table()
        self.assertTrue(True)

    def test_init(self):
        self.game.__init__()
        self.assertTrue(True)

import unittest
import player
import Assets
import bullet
import copy
import pygame.math as pgm
import pygame as pg
import asteroid
from bonus import Bonus
from level_info import LevelInfo


class TextureForTest:
    def __init__(self):
        self.width = 10
        self.height = 10

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class TexturesForTest:
    def __init__(self):
        self.player = pg.Surface((10, 10))
        self.shielded_player = pg.Surface((10, 10))
        self.asteroids_medium = [pg.Surface((10, 10)),
                                 pg.Surface((10, 10)),
                                 pg.Surface((10, 10)),
                                 pg.Surface((10, 10)),
                                 pg.Surface((10, 10))]
        self.asteroids_small = [pg.Surface((10, 10)),
                                pg.Surface((10, 10)),
                                pg.Surface((10, 10)),
                                pg.Surface((10, 10)),
                                pg.Surface((10, 10))]

        self.asteroids_big = [pg.Surface((10, 10)),
                              pg.Surface((10, 10)),
                              pg.Surface((10, 10)),
                              pg.Surface((10, 10)),
                              pg.Surface((10, 10))]

        self.shield_bonus = pg.Surface((10, 10))
        self.score_bonus = pg.Surface((10, 10))
        self.life_bonus = pg.Surface((10, 10))


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
            self.score = 0
            self.bonuses = []
            self.player = player.Player(self)

        @staticmethod
        def get_score_multiplier():
            return 1

    def setUp(self):
        self.game = self.GameForTest(800, 800,
                                     TexturesForTest(), Assets.Audio(),
                                     False, 0)
        self.player = self.game.player

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

    def testCheckBonusCollision(self):
        init_score = self.game.score
        bonus = Bonus(self.game, self.player.head, pgm.Vector2(1, 1))
        self.game.bonuses.append(bonus)
        self.player.check_bonus_collision(self.game, bonus)
        self.assertGreater(self.game.score, init_score)
        self.assertFalse(bonus in self.game.bonuses)

    def testCheckUpdateTexture(self):
        self.player.shield = 101
        self.player.update_texture(self.game)
        self.assertEqual(self.game.textures.shielded_player,
                         self.player.texture)
        self.player.shield = 0
        self.player.update_texture(self.game)
        self.assertEqual(self.game.textures.player,
                         self.player.texture)

import unittest
import pygame.math as pgm
import Assets
import asteroid
import saucer
from level_info import LevelInfo
import copy
import player
import pygame as pg


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


class TestScoreTable(unittest.TestCase):
    def setUp(self):
        self.path = "score_testing.txt"
        self.score_table = ScoreTable(self.path)

    def testUpdateScore(self):
        self.score_table.scores = []
        self.score_table.update_score(40, "ONE")
        self.score_table.update_score(10, "FOU")
        self.score_table.update_score(20, "TWO")
        self.score_table.update_score(30, "THR")
        expected = [("ONE", 40), ("THR", 30), ("TWO", 20), ("FOU", 10)]
        actual = self.score_table.scores
        self.assertEqual(expected, actual)

    def test_init(self):
        self.score_table.scores = []
        self.score_table.__init__("score_testing.txt")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()







