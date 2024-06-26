from multis import *
from obstacles import *
import settings
import pygame, pymunk

class Board():
    def __init__(self, space):
        self.space = space
        self.display_surface = pygame.display.get_surface()

        #obstacles
        self.curr_row_count = 3
        self.final_row_count = 18
        self.obstacles_list = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.updated_coords = OBSTACLE_START

        #sound button
        self.sound_on = pygame.image.load("graphics/soundon.png").convert_alpha()
        self.sound_off = pygame.image.load("graphics/soundoff.png").convert_alpha()
        self.pressing_sound = False
        self.muted = 0
        self.sound_orig_width = self.sound_on.get_width()
        self.sound_orig_height = self.sound_on.get_height()
        self.sound_scaled_width = self.sound_orig_width // 3
        self.sound_scaled_height = self.sound_orig_height // 3
        self.scaled_sound_on = pygame.transform.scale(self.sound_on, (self.sound_scaled_width, self.sound_scaled_height))
        self.scaled_sound_off = pygame.transform.scale(self.sound_off, (self.sound_scaled_width, self.sound_scaled_height))
        self.sound_rect = self.scaled_sound_on.get_rect(center=(WIDTH // 40, HEIGHT // 1.04))
        #chart

        self.chart = pygame.image.load("graphics/chart.png").convert_alpha()
        self.chart_rect = self.chart.get_rect(center=(1848, 1008))
        self.pressing_chart = False

        #reset
        self.reset = pygame.image.load("graphics/reset.png").convert_alpha()
        self.reset_rect = self.chart.get_rect(center=(1752, 998))
        self.pressing_reset = False

        #exit
        self.exit = pygame.image.load("graphics/exit.png").convert_alpha()
        self.exit_rect = self.chart.get_rect(center=(1872, 48))
        self.pressing_exit = False


        #risks

        self.lowrisk_off = pygame.image.load("graphics/lowriskoff.png").convert_alpha()
        self.lowrisk_on = pygame.image.load("graphics/lowriskon.png").convert_alpha()
        self.lowrisk_rect = self.lowrisk_on.get_rect(center=(WIDTH // 32 + 32, HEIGHT // 4 + 32))
        self.pressing_lowrisk = False

        self.mediumrisk_off = pygame.image.load("graphics/mediumriskoff.png").convert_alpha()
        self.mediumrisk_on = pygame.image.load("graphics/mediumriskon.png").convert_alpha()
        self.mediumrisk_rect = self.mediumrisk_on.get_rect(center=(WIDTH // 32 + 292, HEIGHT // 4 + 32))
        self.pressing_mediumrisk = False

        self.highrisk_on = pygame.image.load("graphics/highriskon.png").convert_alpha()
        self.highrisk_off = pygame.image.load("graphics/highriskoff.png").convert_alpha()
        self.highrisk_rect = self.highrisk_on.get_rect(center=(WIDTH // 32 + 552, HEIGHT // 4 + 32))
        self.pressing_highrisk = False

        #play button
        self.play_up = pygame.image.load("graphics/play01.png").convert_alpha()
        self.play_down = pygame.image.load("graphics/play02.png").convert_alpha()
        self.pressing_play = False
        self.play_orig_width = self.play_up.get_width()
        self.play_orig_height = self.play_up.get_height()

        self.play_scaled_width = self.play_orig_width
        self.play_scaled_height = self.play_orig_height
        self.scaled_play_up = pygame.transform.scale(self.play_up, (self.play_scaled_width, self.play_scaled_height))
        self.scaled_play_down = pygame.transform.scale(self.play_down, (self.play_scaled_width, self.play_scaled_height))
        self.play_rect = self.scaled_play_up.get_rect(center=(WIDTH // 6 + 30, HEIGHT // 2 - 150))

        self.segmentA_2 = OBSTACLE_START
        while self.curr_row_count <= self.final_row_count:
            for i in range(self.curr_row_count):
                if self.curr_row_count == 3 and self.updated_coords[0] > OBSTACLE_START[0] + OBSTACLE_PAD:
                    self.segmentB_1 = self.updated_coords
                elif self.curr_row_count == self.final_row_count and i == 0:
                    self.segmentA_1 = self.updated_coords
                elif self.curr_row_count == self.final_row_count and i == self.curr_row_count - 1:
                    self.segmentB_2 = self.updated_coords
                self.obstacles_list.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + OBSTACLE_PAD), self.updated_coords[1])
            self.updated_coords = (int(WIDTH - self.updated_coords[0] + (.5 * OBSTACLE_PAD)), int(self.updated_coords[1] + OBSTACLE_PAD))
            self.curr_row_count += 1
        self.multi_x, self.multi_y = self.updated_coords[0] + OBSTACLE_PAD, self.updated_coords[1]

        self.spawn_segments(self.segmentA_1, self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, self.segmentB_2, self.space)
        self.spawn_segments((self.segmentA_2[0], 0), self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, (self.segmentB_1[0], 0), self.space)

        #spawn multis
        self.spawn_multis()

    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            pos_x, pos_y = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display_surface, (255, 255, 255), (pos_x, pos_y), OBSTACLE_RAD)

    def draw_prev_multi_mask(self):
        multi_mask_surface = pygame.Surface((WIDTH / 4, HEIGHT), pygame.SRCALPHA)
        multi_mask_surface.fill(BG_COLOR)
        right_side_of_board = (WIDTH / 16) * 13
        right_side_pad = right_side_of_board / 130
        mask_y = (HEIGHT / 4) + ((HEIGHT / 4) / 9)
        pygame.draw.rect(multi_mask_surface, (0, 0, 0, 0), (right_side_pad, mask_y, SCORE_RECT, SCORE_RECT * 4), border_radius=30)
        self.display_surface.blit(multi_mask_surface, (right_side_of_board, 0))

    def spawn_multis(self):
        self.multi_amounts = [val[1] for val in settings.multi_rgb.keys()]
        self.rgb_vals = [val for val in settings.multi_rgb.values()]
        for i in range(NUM_MULTIS):
            multi = Multi((self.multi_x, self.multi_y), self.rgb_vals[i], self.multi_amounts[i])
            multi_group.add(multi)
            self.multi_x += OBSTACLE_PAD

    def spawn_obstacle(self, pos, space):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        body.friction = 0.6
        shape = pymunk.Circle(body, OBSTACLE_RAD)
        shape.elasticity = 0.4
        shape.filter = pymunk.ShapeFilter(categories=OBSTACLE_CATEGORY, mask=OBSTACLE_MASK)
        self.space.add(body, shape)
        obstacle = Obstacle(body.position.x, body.position.y)
        self.obstacle_sprites.add(obstacle)
        return shape

    def spawn_segments(self, pointA, pointB, space):
        segment_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, pointA, pointB, 5)
        self.space.add(segment_body, segment_shape)

    def update(self):
        self.draw_obstacles(self.obstacles_list)
        multi_group.draw(self.display_surface)
        multi_group.update()
        if len(list(prev_multi_group)) > 0:
            prev_multi_group.update()
        if len(list(animation_group)) > 0:
            animation_group.update()
        self.draw_prev_multi_mask()
        if self.pressing_play:
            self.display_surface.blit(self.scaled_play_down, (WIDTH // 32, HEIGHT // 3))
        else:
            self.display_surface.blit(self.scaled_play_up, (WIDTH // 32, HEIGHT // 3))
        
        if self.muted % 2 == 0:
            self.display_surface.blit(self.scaled_sound_on, (WIDTH // 128, HEIGHT // 1.08))
        if self.muted % 2 == 1:
            self.display_surface.blit(self.scaled_sound_off, (WIDTH // 128, HEIGHT // 1.08))
        
        if settings.RISK == 0:
            self.display_surface.blit(self.lowrisk_on, (WIDTH // 32, HEIGHT // 4))
            self.display_surface.blit(self.mediumrisk_off, (WIDTH // 32 + 260, HEIGHT // 4))
            self.display_surface.blit(self.highrisk_off, (WIDTH // 32 + 520, HEIGHT // 4))

        if settings.RISK == 1:
            self.display_surface.blit(self.lowrisk_off, (WIDTH // 32, HEIGHT // 4))
            self.display_surface.blit(self.mediumrisk_on, (WIDTH // 32 + 260, HEIGHT // 4))
            self.display_surface.blit(self.highrisk_off, (WIDTH // 32 + 520, HEIGHT // 4))

        if settings.RISK == 2:
            self.display_surface.blit(self.lowrisk_off, (WIDTH // 32, HEIGHT // 4))
            self.display_surface.blit(self.mediumrisk_off, (WIDTH // 32 + 260, HEIGHT // 4))
            self.display_surface.blit(self.highrisk_on, (WIDTH // 32 + 520, HEIGHT // 4))

        #balance
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = self.font.render(f"Balance: {settings.BALANCE}$" , True, (255, 255, 255))
        self.display_surface.blit(self.text_surface, (30, 60))

        #bet amount
        self.pressing_bet = False
        self.bet_amount = self.font.render(settings.BET_TEXT, True, settings.COLOR)
        self.bet_rect = pygame.Rect(30, 100, 100, 50)
        self.text_bet = self.font.render(f"BET:", True, settings.COLOR)
        self.display_surface.blit(self.text_bet, (30, 110))
        self.display_surface.blit(self.bet_amount, (100, 110))
        
        #auto
        self.pressing_auto = False
        self.auto_amount = self.font.render(settings.AUTO_TEXT, True, settings.COLOR_AUTO)
        self.auto_rect = pygame.Rect(30, 150, 100, 50)
        self.text_auto = self.font.render(f"AUTO", True, settings.COLOR_AUTO)


        self.display_surface.blit(self.text_auto, (30, 150))
        if settings.ACTIVE_AUTO == True:
            self.display_surface.blit(self.font.render(f":", True, settings.COLOR_AUTO), (120, 150))
            self.display_surface.blit(self.auto_amount, (130, 150))

        #welcome
        self.display_surface.blit(self.font.render(f"Welcome,", True, settings.WHITE), (30, 10))
        self.display_surface.blit(self.font.render(settings.USERNAME, True, settings.WHITE), (170, 10))

        #chart
        self.display_surface.blit(self.chart, (1800, 960))

        #warning
        
        
        if settings.enough_balance == False:
            self.text_warning = self.font.render(f"No balance!", True, (255, 0, 0))
            self.display_surface.blit(self.text_warning, (500, 60))

        #reset stats

        self.display_surface.blit(self.reset, (1704, 970))

        #exit

        self.display_surface.blit(self.exit, (1824, 0))
    
        

