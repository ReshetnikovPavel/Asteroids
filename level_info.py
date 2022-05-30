import pygame as pg


class LevelInfo:
    def __init__(self, level_count, ticks_to_next_level,
                 level_start_tick,
                 asteroids_timing, saucer_timing,
                 asteroid_speed_coefficient,
                 saucer_fire_timing, game):

        self.level_count = level_count
        self.ticks_to_next_level = ticks_to_next_level
        self.level_start_tick = level_start_tick
        self.asteroids_timing = asteroids_timing
        self.saucer_timing = saucer_timing
        self.asteroid_speed_coefficient = asteroid_speed_coefficient
        self.saucer_fire_timing = saucer_fire_timing
        self.game = game

    def move_to_next_level(self, level_start_tick):
        self.level_count += 1
        self.ticks_to_next_level *= 1.5
        self.asteroids_timing //= 1.1
        self.saucer_timing //= 1.1
        self.asteroid_speed_coefficient *= 1.1
        self.saucer_fire_timing //= 1.5
        self.level_start_tick = level_start_tick
        # print(f'next level {self.level_count}')
        # print(f'asteroid_speed_coeff{self.asteroid_speed_coefficient}')
        if self.game.is_audio_on:
            pg.mixer.Sound.play(self.game.audio.levelup)
        self.game.score += (self.level_count - 1) * 10

    def check_next_level(self, current_tick):
        if current_tick - self.level_start_tick > self.ticks_to_next_level:
            self.move_to_next_level(current_tick)
