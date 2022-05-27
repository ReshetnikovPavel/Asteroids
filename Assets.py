import pygame as pg


class Textures:
    def __init__(self):
        self.player = pg.image.load(r'Assets\Textures\player.png')
        self.player_no_texture = pg.image.load(r'Assets\Textures'
                                               r'\player_no_texture.png')
        self.saucer = pg.image.load(r'Assets\Textures\saucer.png')
        self.asteroids_big = [
            pg.image.load(r'Assets\Textures\big_1.png'),
            pg.image.load(r'Assets\Textures\big_2.png'),
            pg.image.load(r'Assets\Textures\big_3.png'),
            pg.image.load(r'Assets\Textures\big_4.png')]
        self.asteroids_medium = [
            pg.image.load(r'Assets\Textures\medium_1.png'),
            pg.image.load(r'Assets\Textures\medium_2.png'),
            pg.image.load(r'Assets\Textures\medium_3.png'),
            pg.image.load(r'Assets\Textures\medium_4.png')]
        self.asteroids_small = [
            pg.image.load(r'Assets\Textures\small_1.png'),
            pg.image.load(r'Assets\Textures\small_2.png'),
            pg.image.load(r'Assets\Textures\small_3.png'),
            pg.image.load(r'Assets\Textures\small_4.png')]
        self.life_bonus = pg.image.load(r'Assets\Textures\life_bonus.png')
        self.shield_bonus = pg.image.load(r'Assets\Textures\shield_bonus.png')
        self.point_bonus = pg.image.load(r'Assets\Textures\point_bonus.png')


class Audio:
    def __init__(self):
        pg.mixer.init()
        self.explodes = [
            pg.mixer.Sound(r'Assets\Audio\EXPLODE1.WAV'),
            pg.mixer.Sound(r'Assets\Audio\EXPLODE2.WAV'),
            pg.mixer.Sound(r'Assets\Audio\EXPLODE3.WAV')]
        self.fire = pg.mixer.Sound(r'Assets\Audio\FIRE.WAV')
        self.life = pg.mixer.Sound(r'Assets\Audio\LIFE.WAV')
        self.l_saucer = pg.mixer.Sound(r'Assets\Audio\LSAUCER.WAV')
        self.s_fire = pg.mixer.Sound(r'Assets\Audio\SFIRE.WAV')
        self.s_saucer = pg.mixer.Sound(r'Assets\Audio\SSAUCER.WAV')
        self.thrust = pg.mixer.Sound(r'Assets\Audio\THRUST.WAV')
