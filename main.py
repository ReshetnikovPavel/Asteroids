import random
import pygame as pg
import pygame.math
import Assets
from asteroid import Asteroid
from level_info import LevelInfo
from player import Player
from saucer import Saucer
from score_table import ScoreTable

pygame.init()


class Game:
    def __init__(self):
        self.is_audio_on = False
        self.textures = Assets.Textures()
        self.audio = Assets.Audio()
        self.screen_width = 800
        self.screen_height = 800
        self.clock = pg.time.Clock()
        self.asteroids = []
        self.saucers = []
        self.bonuses = []
        self.count = 0
        self.is_run = True
        self.game_over = True
        try:
            self.screen = pg.display.set_mode(
                (self.screen_width, self.screen_height),
                pg.FULLSCREEN | pg.SCALED)
        except pygame.error as message:
            pass

        self.player = Player(self)
        self.score = 0
        self.font = pygame.font.Font(r'Assets/Hyperspace.otf', 36)
        self.title_font = pygame.font.Font(r'Assets/Hyperspace.otf', 60)
        self.score_table = ScoreTable("score.txt")
        self.draw = self.draw_main_menu
        self.handle_events = self.handle_menu_events
        self.player_name = ''
        self.double_score = 0
        self.level_info = LevelInfo(1, 1500, 0, 100, 1055, 1, 300, self)
        self.elements_drawn = 0
        self.score_entries_drawn = 0

    def run(self):
        pg.display.set_caption('Asteroids')
        while True:
            self.in_run()

    def in_run(self):
        self.clock.tick(60)
        self.count += 1
        if self.player.lives < 0 and not self.game_over:
            self.end_game()

        if not self.game_over:
            if self.count % self.level_info.asteroids_timing == 0:
                random_number = random.choice([1, 1, 1, 2, 2, 3])
                self.asteroids.append(Asteroid(self, random_number))

            if self.count % self.level_info.saucer_timing == 0:
                self.saucers.append(Saucer(self))
        try:
            self.handle_controls()
            self.update()
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw()
            pg.display.update()

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                pg.quit()

        except pygame.error as message:
            pass

    def update(self):
        self.level_info.check_next_level(self.count)
        self.player.update(self)
        self.loop_object(self.player)
        for bullet in self.player.bullets:
            self.loop_object(bullet)
            bullet.update()
            if bullet.life <= 0:
                self.player.bullets.remove(bullet)

        for asteroid in self.asteroids:
            asteroid.check_bullet_collision(self)
            self.player.check_asteroid_collision(self, asteroid)
            self.loop_object(asteroid)
            asteroid.move()

        for saucer in self.saucers:
            for asteroid in self.asteroids:
                saucer.check_asteroid_collision(self, asteroid)
            for bullet in self.player.bullets:
                saucer.check_bullet_collision(self, bullet)
            self.player.check_asteroid_collision(self, saucer)
            saucer.move(self)
            for bullet in saucer.bullets:
                self.player.check_bullet_collision(self, bullet)
                self.loop_object(bullet)
                bullet.update()
                if bullet.life <= 0:
                    saucer.bullets.remove(bullet)

        for bonus in self.bonuses:
            bonus.move(self)
            self.loop_object(bonus)
            self.player.check_bonus_collision(self, bonus)
            if bonus.life <= 0:
                self.bonuses.remove(bonus)

        if self.double_score > 0:
            self.double_score -= 1

    def draw_game(self):
        try:
            self.score_text = self.font.render('Score: ' + str(self.score), True,
                                          (255, 255, 255))
            self.best_score_text = self.font.render(
                'Best: ' + str(self.score_table.value), True,
                (255, 255, 255))
            self.lives_text = self.font.render('Lives: ' + str(self.player.lives),
                                          True,
                                          (255, 255, 255))
            level_text = self.font.render(
                'Level ' + str(self.level_info.level_count), True,
                (255, 255, 255))
            self.screen.blit(self.score_text,
                             (self.screen_width - 500,
                              35 + self.score_text.get_height()))
            self.screen.blit(self.best_score_text,
                             (self.screen_width - 500,
                              30))
            self.screen.blit(level_text,
                             (self.screen_width - 20 - level_text.get_width(),
                              30))
            self.screen.blit(self.lives_text,
                             (20,
                              30))
        except AttributeError or pygame.error as message:
            pass
        for asteroid in self.asteroids:
            try:
                asteroid.draw(self.screen)
            except AttributeError or pygame.error as message:
                pass
            self.elements_drawn += 1
        for bullet in self.player.bullets:
            try:
                bullet.draw(self)
            except AttributeError or pygame.error as message:
                pass
            self.elements_drawn += 1
        for saucer in self.saucers:
            try:
                saucer.draw(self.screen)
            except AttributeError or pygame.error as message:
                pass
            self.elements_drawn += 1
            for bullet in saucer.bullets:
                try:
                    bullet.draw(self)
                except AttributeError or pygame.error as message:
                    pass
                self.elements_drawn += 1
        for bonus in self.bonuses:
            try:
                bonus.draw(self)
            except AttributeError or pygame.error as message:
                pass
            self.elements_drawn += 1
        try:
            self.player.draw(self)
        except AttributeError or pygame.error as message:
            pass
        self.elements_drawn += 1

    def draw_death_screen(self):
        self.score_text = self.font.render('Score: ' + str(self.score), True,
                                      (255, 255, 255))
        self.best_score_text = self.font.render(
            'Best: ' + str(self.score_table.value), True,
            (255, 255, 255))
        self.level_text = self.font.render(
            'Level ' + str(self.level_info.level_count), True,
            (255, 255, 255))
        self.gameover_text = self.font.render('GAME OVER', True,
                                         (255, 255, 255))
        self.gameover_text_2 = self.font.render('Please enter your name:', True,
                                           (255, 255, 255))
        self.press_enter_text = self.font.render('(Press ENTER to continue)', True,
                                            (255, 255, 255))
        self.name_text = self.font.render(self.player_name, True, (255, 255, 255))
        self.screen.blit(self.score_text,
                         (self.screen_width - 500,
                          35 + self.score_text.get_height()))
        self.screen.blit(self.best_score_text,
                         (self.screen_width - 500,
                          30))
        self.screen.blit(self.level_text,
                         (self.screen_width - 20 - self.level_text.get_width(),
                          30))
        self.screen.blit(self.gameover_text,
                         self._get_destination_for_text_header(
                             self.gameover_text.get_width(),
                             self.gameover_text.get_height(), -50))
        self.screen.blit(self.gameover_text_2,
                         self._get_destination_for_text_header(
                             self.gameover_text_2.get_width(),
                             self.gameover_text_2.get_height(),
                             self.gameover_text_2.get_height() - 50))
        self.screen.blit(self.name_text, self._get_destination_for_text_header(
            self.name_text.get_width(),
            self.gameover_text_2.get_height(), self.gameover_text_2.get_height()))
        if len(self.player_name) > 0:
            width = self.screen_width / 2 - self.press_enter_text.get_width() / 2
            height = self.screen_height - self.press_enter_text.get_height() - 30
            self.screen.blit(self.press_enter_text, (width, height))

    def _get_destination_for_text_header(self, width, height, offset_height):
        return self.screen_width / 2 - width / 2, \
               self.screen_height / 2 - height / 2 + offset_height

    def _get_destination_for_text_next_entry(self, width, height, i,
                                             horizontal_spacing,
                                             vertical_spacing):
        return self.screen_width / 2 - width / 2 + horizontal_spacing, \
               (vertical_spacing + height) * (i + 1)

    def draw_score_table(self):
        vertical_spacing = 30
        horizontal_spacing = 100
        try:
            press_enter_text = self.font.render('(Press ENTER to restart)',
                                                True, (255, 255, 255))
        except pygame.error as message:
            pass
        count = len(self.score_table.scores)
        for i in range(count):
            name = self.score_table.scores[i][0]
            score = str(self.score_table.scores[i][1])
            self.score_entries_drawn += 1
            try:
                name_text = self.font.render(name, True, (255, 255, 255))
                score_text = self.font.render(score, True, (255, 255, 255))
                entry_width = name_text.get_width() + score_text.get_width()
                entry_width += horizontal_spacing
                self.screen.blit(name_text,
                                 self._get_destination_for_text_next_entry(
                                     entry_width, name_text.get_height(), i,
                                     0, vertical_spacing))
                self.screen.blit(score_text,
                                 self._get_destination_for_text_next_entry(
                                     entry_width, name_text.get_height(), i,
                                     horizontal_spacing, vertical_spacing))
            except Exception or pygame.error as message:
                pass
        try:
            width = self.screen_width / 2 - press_enter_text.get_width() / 2
            height = self.screen_height - press_enter_text.get_height() - 30
            self.screen.blit(press_enter_text, (width, height))
        except Exception or pygame.error as message:
            pass

    def draw_main_menu(self):
        title_text = self.title_font.render('Asteroids', True,
                                            (255, 255, 255))
        press_enter_text = self.font.render('Press ENTER to start', True,
                                            (255, 255, 255))

        width = self.screen_width / 2 - press_enter_text.get_width() / 2
        height = self.screen_height - press_enter_text.get_height() - 30
        height *= 3 / 4
        self.screen.blit(press_enter_text, (width, height))
        self.screen.blit(title_text, self._get_destination_for_text_header(
            title_text.get_width(), title_text.get_height(), 0))

    def end_game(self):
        self.game_over = True
        self.draw = self.draw_death_screen
        self.handle_events = self.handle_death_events
        # pg.mixer.music.stop()
        # pg.mixer.music.load(r'Assets\Audio\DEFEAT.WAV')
        # pg.mixer.music.play(-1)
        print("You've met with a terrible fate, haven't you?")

    def start_game(self):
        self.draw = self.draw_game
        self.handle_events = self.handle_game_events
        self.game_over = False
        # pg.mixer.music.stop()
        # pg.mixer.music.load(r'Assets\Audio\MUSIC.WAV')
        # pg.mixer.music.play(-1)

    def handle_controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.turn_left()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.turn_right()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.move_forward(game)

    def handle_game_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.game_over:
                        self.player.fire(self)

    def handle_death_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.score_table.update_score(self.score, self.player_name)
                    self.draw = self.draw_score_table
                    self.handle_events = self.handle_table_events
                elif event.key == pg.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key != pg.K_SPACE and len(self.player_name) < 3:
                    self.player_name += event.unicode

    def handle_table_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.__init__()

    def handle_menu_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.start_game()

    def loop_object(self, obj):
        if obj.position.x > self.screen_width + obj.height:
            obj.position.x = -obj.height
        elif obj.position.x < -obj.height:
            obj.position.x = self.screen_width + obj.height
        if obj.position.y > self.screen_height + obj.height:
            obj.position.y = -obj.height
        elif obj.position.y < -obj.height:
            obj.position.y = self.screen_height + obj.height

    def get_score_multiplier(self):
        if self.double_score > 0:
            return 2
        else:
            return 1


# On start
if __name__ == '__main__':
    game = Game()
    game.run()
