import pygame.math as pgm
from itertools import combinations
import numpy as np


def check_collision(outer, inner):
    out_pos = outer.position
    in_pos = inner.position
    center_x = out_pos.x <= in_pos.x <= out_pos.x + outer.width
    edge_x = out_pos.x <= in_pos.x + inner.width <= out_pos.x + outer.width
    center_y = out_pos.y <= in_pos.y <= out_pos.y + outer.height
    edge_y = out_pos.y <= in_pos.y + inner.height <= out_pos.y + outer.height
    return (center_x or edge_x) and (center_y or edge_y)


def check_player_triangular_collision(player, box_object):
    point1 = player.head
    norm_dir = pgm.Vector2.normalize(player.direction)
    base = point1 - norm_dir * player.height
    perpendicular_to_dir = pgm.Vector2(-norm_dir.y, norm_dir.x).normalize()
    point2 = base - perpendicular_to_dir * player.width/2
    point3 = base + perpendicular_to_dir * player.width/2
    vertices = [point1, point2, point3]
    box_vertices = [box_object.position,
                    box_object.position + pgm.Vector2(box_object.width, 0),
                    box_object.position + pgm.Vector2(0, box_object.height),
                    box_object.position
                    + pgm.Vector2(box_object.width, box_object.height)]
    for v in box_vertices:
        if _is_point_in_triangle(vertices, v):
            return True
    for v in vertices:
        if _is_point_in_box(box_object, v):
            return True
    return False


def _is_point_in_triangle(vertices, point):
    vector_edges = list(map(lambda v: v - point, vertices))
    areas = []
    for vector1, vector2 in combinations(vector_edges, 2):
        vector1 = np.array([vector1])
        vector2 = np.array([vector2])
        cross_product = np.cross(vector1, vector2)
        area = np.linalg.norm(cross_product) / 2
        areas.append(area)

    triangle_v1 = vertices[1] - vertices[0]
    triangle_v2 = vertices[2] - vertices[0]
    cross_product = np.cross(triangle_v1, triangle_v2)
    triangle_area = np.linalg.norm(cross_product) / 2
    return abs(triangle_area - sum(areas)) < 0.001


def _is_point_in_box(box_object, point):
    x = box_object.position.x
    y = box_object.position.y
    width = box_object.width
    return x <= point.x <= x + width and y <= point.y <= y + width
