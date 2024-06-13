from ball import Ball
from board import *
from multis import *
import time
import settings
import ctypes, pygame, pymunk, random, sys
import matplotlib.pyplot as plt
import os
import json


ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)
        self.balls_played = 0

    def update_user_data(username, new_balance):
        username_str = str(username)
        with open('users.json', 'r+') as file:
            data = json.load(file)
            data[username_str]['balance'] = new_balance
            file.seek(0)
            json.dump(data, file, indent=4)

    def run(self):
        self.start = time.time()
        self.start_time = pygame.time.get_ticks()
        while True:
            self.now = time.time()
            if self.now - self.start >= 7:
                settings.BALLS = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.username = settings.USERNAME
                    Game.update_user_data(settings.USERNAME, settings.BALANCE)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and settings.BALLS == 0:
                    if settings.ACTIVE == True:
                        if event.key == pygame.K_BACKSPACE:
                           settings.BET_TEXT = settings.BET_TEXT[:-1]
                        else:
                            if event.unicode.isdigit() or event.unicode == '.':
                                if event.unicode == '.' and '.' in settings.BET_TEXT:
                                    continue
                                if float(settings.BET_TEXT + event.unicode) <= settings.BALANCE: 
                                    settings.BET_TEXT += event.unicode
                                    settings.BET = float(settings.BET_TEXT)
                
                if event.type == pygame.KEYDOWN:
                    if settings.ACTIVE_AUTO == True:
                        if event.key == pygame.K_BACKSPACE:
                           settings.AUTO_TEXT = settings.AUTO_TEXT[:-1]
                        else:
                            if event.unicode.isdigit():
                                settings.AUTO_TEXT += event.unicode
                                settings.AUTO = int(settings.AUTO_TEXT)
                        if event.key == pygame.K_RETURN:
                            settings.AUTO = int(settings.AUTO_TEXT)
                            if settings.AUTO * settings.BET <= settings.BALANCE:
                                self.start = self.now
                                settings.enough_balance = True
                                self.drop = settings.AUTO
                                settings.BALLS = settings.BALLS + settings.AUTO
                                for i in range (self.drop):
                                    settings.BALANCE = round(settings.BALANCE - settings.BET, 2)
                                    random_x = WIDTH//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                                    click.play()
                                    self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                                    self.ball_group.add(self.ball)
                            else:
                                settings.enough_balance = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.board.play_rect.collidepoint(mouse_pos):
                        self.board.pressing_play = True
                    else:
                        self.board.pressing_play = False

                    if self.board.sound_rect.collidepoint(mouse_pos):
                        self.board.pressing_sound = True
                    else:
                        self.board.pressing_sound = False

                    if self.board.lowrisk_rect.collidepoint(mouse_pos):
                        self.board.pressing_lowrisk = True
                    else:
                        self.board.pressing_lowrisk = False
                    
                    if self.board.mediumrisk_rect.collidepoint(mouse_pos):
                        self.board.pressing_mediumrisk = True
                    else:
                        self.board.pressing_mediumrisk = False

                    if self.board.highrisk_rect.collidepoint(mouse_pos):
                        self.board.pressing_highrisk = True
                    else:
                        self.board.pressing_highrisk = False

                    if self.board.chart_rect.collidepoint(mouse_pos):
                        self.board.pressing_chart = True
                    else:
                        self.board.pressing_chart = False

                    if self.board.reset_rect.collidepoint(mouse_pos):
                        self.board.pressing_reset = True
                    else:
                        self.board.pressing_reset = False

                    if self.board.bet_rect.collidepoint(mouse_pos):
                        self.board.pressing_bet = True
                    else:
                        self.board.pressing_bet = False

                    if self.board.exit_rect.collidepoint(mouse_pos):
                        self.board.pressing_exit = True
                    else:
                        self.board.pressing_exit = False
             
                    if self.board.bet_rect.collidepoint(mouse_pos):
                        settings.ACTIVE = True
                    else:
                        settings.ACTIVE = False

                    if self.board.auto_rect.collidepoint(mouse_pos):
                        settings.ACTIVE_AUTO = True
                    else:
                        settings.ACTIVE_AUTO = False              

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_play:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.play_rect.collidepoint(mouse_pos):
                        self.start = self.now
                        settings.BET = float(settings.BET_TEXT)
                        if settings.BALANCE - settings.BET >= 0:
                            settings.enough_balance = True
                            settings.BALANCE = round(settings.BALANCE - settings.BET, 2)
                            random_x = WIDTH//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                            click.play()
                            self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                            self.ball_group.add(self.ball)
                            settings.BALLS = settings.BALLS + 1
                            self.board.pressing_play = False
                        else:
                            settings.enough_balance = False
                            self.board.pressing_play = False
                    else:
                        self.board.pressing_play = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_sound: 
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.sound_rect.collidepoint(mouse_pos):
                        self.board.muted = self.board.muted + 1
                        self.board.pressing_sound = False
                    else:
                        self.board.pressing_sound = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_reset: 
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.reset_rect.collidepoint(mouse_pos):
                        settings.balance_log.clear()
                        settings.balance_log = [settings.BALANCE]
                        self.board.pressing_reset = False
                    else:
                        self.board.pressing_reset = False
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_exit: 
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        self.username = settings.USERNAME
                        Game.update_user_data(settings.USERNAME, settings.BALANCE)
                        os.system("python start.py")
                        self.board.pressing_exit = False
                    else:
                        self.board.pressing_exit = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_lowrisk:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.lowrisk_rect.collidepoint(mouse_pos) and settings.BALLS == 0:                       
                        settings.RISK = 0
                        for multi in list(multi_group):
                            multi_group.remove(multi)
                        settings.multi_rgb.clear()
                        settings.multi_rgb = {
                            (0, 16): (255, 0, 0),
                            (1, 9): (255, 30, 0),
                            (2, 2): (255, 60, 0),
                            (3, 1.4): (255, 90, 0),
                            (4, 1.4): (255, 120, 0),
                            (5, 1.2): (255, 150, 0),
                            (6, 1.1): (255, 180, 0),
                            (7, 1): (255, 210, 0),
                            (8, 0.5): (255, 240, 0),
                            (9, 1): (255, 210, 0),
                            (10, 1.1): (255, 180, 0),
                            (11, 1.2): (255, 150, 0),
                            (12, 1.4): (255, 120, 0),
                            (13, 1.4): (255, 90, 0),
                            (14, 2): (255, 60, 0),
                            (15, 9): (255, 30, 0),
                            (16, 16): (255, 0, 0),
                            }
                        Board(self.space)
                        self.board.pressing_lowrisk = False
                    else:
                        self.board.pressing_lowrisk = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_mediumrisk:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.mediumrisk_rect.collidepoint(mouse_pos) and settings.BALLS == 0:
                        settings.RISK = 1
                        for multi in list(multi_group):
                            multi_group.remove(multi)
                        
                        settings.multi_rgb.clear()
                        settings.multi_rgb = {
                            (0, 110): (255, 0, 0),
                            (1, 41): (255, 30, 0),
                            (2, 10): (255, 60, 0),
                            (3, 5): (255, 90, 0),
                            (4, 3): (255, 120, 0),
                            (5, 1.5): (255, 150, 0),
                            (6, 1): (255, 180, 0),
                            (7, 0.5): (255, 210, 0),
                            (8, 0.3): (255, 240, 0),
                            (9, 0.5): (255, 210, 0),
                            (10, 1): (255, 180, 0),
                            (11, 1.5): (255, 150, 0),
                            (12, 3): (255, 120, 0),
                            (13, 5): (255, 90, 0),
                            (14, 10): (255, 60, 0),
                            (15, 41): (255, 30, 0),
                            (16, 110): (255, 0, 0),
                            }
                        Board(self.space)
                        self.board.pressing_mediumrisk = False
                    else:
                        self.board.pressing_mediumrisk = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_highrisk:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.highrisk_rect.collidepoint(mouse_pos) and settings.BALLS == 0:
                        settings.RISK = 2
                        for multi in list(multi_group):
                            multi_group.remove(multi)
                        settings.multi_rgb.clear()
                        settings.multi_rgb = {
                            (0, 1000): (255, 0, 0),
                            (1, 130): (255, 30, 0),
                            (2, 26): (255, 60, 0),
                            (3, 9): (255, 90, 0),
                            (4, 4): (255, 120, 0),
                            (5, 2): (255, 150, 0),
                            (6, 0.2): (255, 180, 0),
                            (7, 0.2): (255, 210, 0),
                            (8, 0.2): (255, 240, 0),
                            (9, 0.2): (255, 210, 0),
                            (10, 0.2): (255, 180, 0),
                            (11, 2): (255, 150, 0),
                            (12, 4): (255, 120, 0),
                            (13, 9): (255, 90, 0),
                            (14, 26): (255, 60, 0),
                            (15, 130): (255, 30, 0),
                            (16, 1000): (255, 0, 0),
                        }
                        Board(self.space)
                        self.board.pressing_highrisk = False
                    else:
                        self.board.pressing_highrisk = False
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_chart: 
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.chart_rect.collidepoint(mouse_pos) and settings.BALLS == 0:
                        self.indexes = list(range(len(settings.balance_log)))
                        if settings.balance_log[-1] >= settings.balance_log[0]:
                            plt.plot(self.indexes, settings.balance_log, color = 'green')
                        else:
                            plt.plot(self.indexes, settings.balance_log, color = 'red')
                        plt.title('Balance chart')
                        plt.xlabel('Bet #')
                        plt.ylabel('Balance')
                        plt.show()
                        self.board.pressing_chart = False
                    else:
                        self.board.pressing_chart = False
            
            self.screen.fill(BG_COLOR)

            self.delta_time = self.clock.tick(FPS) / 1000.0

            self.space.step(self.delta_time)
            self.board.update()
            self.ball_group.update()

            # sound volume logic

            if self.board.muted % 2 == 1:
                click.set_volume(0)
                sound01.set_volume(0)
                sound02.set_volume(0)
                sound03.set_volume(0)
                sound04.set_volume(0)
                sound05.set_volume(0)
                sound06.set_volume(0)
                sound07.set_volume(0)

            if self.board.muted % 2 == 0:
                click.set_volume(1)
                sound01.set_volume(0.2)
                sound02.set_volume(0.3)
                sound03.set_volume(0.4)
                sound04.set_volume(0.5)
                sound05.set_volume(0.6)
                sound06.set_volume(0.7)
                sound07.set_volume(0.8)

            if settings.ACTIVE == True:
                settings.COLOR = settings.GREEN
            else:
                settings.COLOR = settings.WHITE

            if settings.ACTIVE_AUTO == True:
                settings.COLOR_AUTO = settings.GREEN
            else:
                settings.COLOR_AUTO = settings.LIGHT_BLUE                     
                
            pygame.display.update()

if __name__ == '__main__':
            game = Game()
            game.run()

    
