import pygame as pg
import os


class Textures:
    def __init__(self):
        print(os.getcwd())
        self.player = pg.image.load('Assets/Textures/player.png')
        self.player_no_texture = pg.image.load('Assets/Textures'
                                               '/player_no_texture.png')
        self.saucer = pg.image.load('Assets/Textures/saucer.png')
        self.asteroids_big = [
            pg.image.load('Assets/Textures/big_1.png'),
            pg.image.load('Assets/Textures/big_2.png'),
            pg.image.load('Assets/Textures/big_3.png'),
            pg.image.load('Assets/Textures/big_4.png')]
        self.asteroids_medium = [
            pg.image.load('Assets/Textures/medium_1.png'),
            pg.image.load('Assets/Textures/medium_2.png'),
            pg.image.load('Assets/Textures/medium_3.png'),
            pg.image.load('Assets/Textures/medium_4.png')]
        self.asteroids_small = [
            pg.image.load('Assets/Textures/small_1.png'),
            pg.image.load('Assets/Textures/small_2.png'),
            pg.image.load('Assets/Textures/small_3.png'),
            pg.image.load('Assets/Textures/small_4.png')]
        self.life_bonus = pg.image.load('Assets/Textures/life_bonus.png')
        self.shield_bonus = pg.image.load('Assets/Textures/shield_bonus.png')
        self.score_bonus = pg.image.load('Assets/Textures/score_bonus.png')
        self.shielded_player = pg.image.load('Assets/Textures'
                                             '/shielded_player.png')


class Audio:
    def __init__(self):
        pg.mixer.init()
        self.explodes = [
            pg.mixer.Sound('Assets/Audio/EXPLODE1.WAV'),
            pg.mixer.Sound('Assets/Audio/EXPLODE2.WAV'),
            pg.mixer.Sound('Assets/Audio/EXPLODE3.WAV')]
        self.fire = pg.mixer.Sound('Assets/Audio/FIRE.WAV')
        self.life = pg.mixer.Sound('Assets/Audio/LIFE.WAV')
        self.l_saucer = pg.mixer.Sound('Assets/Audio/LSAUCER.WAV')
        self.s_fire = pg.mixer.Sound('Assets/Audio/SFIRE.WAV')
        self.s_saucer = pg.mixer.Sound('Assets/Audio/SSAUCER.WAV')
        self.thrust = pg.mixer.Sound('Assets/Audio/THRUST.WAV')
        self.bonus = pg.mixer.Sound('Assets/Audio/BONUS.WAV')
        self.levelup = pg.mixer.Sound('Assets/Audio/LEVELUP.WAV')
