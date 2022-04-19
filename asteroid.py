from Assets import Textures
import random
import main
import pygame.math as m


class Asteroid:
    def __init__(self, rank):  # rank - размер астероида
        self.rank = rank
        self.texture = self._set_texture(rank)
        self.width = 50 * rank
        self.height = 50 * rank
        self.spawn_point = random.choice(
            [(random.randrange(0, main.screen_width - self.width),
              random.choice([-1 * self.height - 5, main.screen_height + 5])),
             (random.choice([-1 * self.width - 5, main.screen_width + 5]),
              random.randrange(0, main.screen_height - self.height))])

        self.x, self.y = self.spawn_point
        self.direction = m.Vector2(1 if self.x < main.screen_width//2 else -1,
                                   1 if self.y < main.screen_height//2 else -1)

        self.velocity = m.Vector2(self.direction.x * random.randrange(1, 3),
                                  self.direction.y * random.randrange(1, 3))

    @staticmethod
    def _set_texture(rank):
        textures = Textures()
        random_number = random.randint(0, 3)
        if rank == 1:
            return textures.asteroids_small[random_number]
        elif rank == 2:
            return textures.asteroids_medium[random_number]
        elif rank == 3:
            return textures.asteroids_big[random_number]

    def draw(self, window):
        window.blit(self.texture, (self.x, self.y))  # TODO
