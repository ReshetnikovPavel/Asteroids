import unittest
import collision
import pygame.math as pgm
import asteroid


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
        self.assertFalse(collision._is_point_in_triangle(self.triangle_vertices,
                                                         point))

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
        self.assertTrue(collision.check_player_triangular_collision(self.player,
                                                                    box))

    def testPlayerTriangleAndBoxDoNotCollideCollision(self):
        box = self.BoxForTest(position=pgm.Vector2(100, 100),
                              width=8,
                              height=5)
        self.assertFalse(collision.check_player_triangular_collision(
            self.player, box))


if __name__ == '__main__':
    unittest.main()
