from ball import Ball
from board import *
from multis import *
from settings import *
import ctypes, pygame, pymunk, random, sys

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

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_play:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.play_rect.collidepoint(mouse_pos):
                        random_x = WIDTH//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                        click.play()
                        self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                        self.ball_group.add(self.ball)
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

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()