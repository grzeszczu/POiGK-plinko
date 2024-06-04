from multis import *
from obstacles import *
from settings import *
import pygame, pymunk

class Board():
    def __init__(self, space):
        self.space = space
        self.display_surface = pygame.display.get_surface()

        # Obstacles
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

        # Play button
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

        # Get second point for segmentA
        self.segmentA_2 = OBSTACLE_START
        while self.curr_row_count <= self.final_row_count:
            for i in range(self.curr_row_count):
                # Get first point for segmentB
                if self.curr_row_count == 3 and self.updated_coords[0] > OBSTACLE_START[0] + OBSTACLE_PAD:
                    self.segmentB_1 = self.updated_coords
                # Get first point for segmentA
                elif self.curr_row_count == self.final_row_count and i == 0:
                    self.segmentA_1 = self.updated_coords
                # Get second point for segmentB
                elif self.curr_row_count == self.final_row_count and i == self.curr_row_count - 1:
                    self.segmentB_2 = self.updated_coords
                self.obstacles_list.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + OBSTACLE_PAD), self.updated_coords[1])
            self.updated_coords = (int(WIDTH - self.updated_coords[0] + (.5 * OBSTACLE_PAD)), int(self.updated_coords[1] + OBSTACLE_PAD))
            self.curr_row_count += 1
        self.multi_x, self.multi_y = self.updated_coords[0] + OBSTACLE_PAD, self.updated_coords[1]

        # Segments (boundaries on side of obstacles)
        self.spawn_segments(self.segmentA_1, self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, self.segmentB_2, self.space)
        # Segments at top of obstacles
        self.spawn_segments((self.segmentA_2[0], 0), self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, (self.segmentB_1[0], 0), self.space)

        # Spawn multis
        self.spawn_multis()

    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            pos_x, pos_y = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display_surface, (255, 255, 255), (pos_x, pos_y), OBSTACLE_RAD)

    # Used to give a border radius to previous multi display on right side
    def draw_prev_multi_mask(self):
        multi_mask_surface = pygame.Surface((WIDTH / 4, HEIGHT), pygame.SRCALPHA)
        multi_mask_surface.fill(BG_COLOR)
        right_side_of_board = (WIDTH / 16) * 13
        right_side_pad = right_side_of_board / 130
        mask_y = (HEIGHT / 4) + ((HEIGHT / 4) / 9)
        pygame.draw.rect(multi_mask_surface, (0, 0, 0, 0), (right_side_pad, mask_y, SCORE_RECT, SCORE_RECT * 4), border_radius=30)
        self.display_surface.blit(multi_mask_surface, (right_side_of_board, 0))

    def spawn_multis(self):
        self.multi_amounts = [val[1] for val in multi_rgb.keys()]
        self.rgb_vals = [val for val in multi_rgb.values()]
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
        segment_shape = pymunk.Segment(segment_body, pointA, pointB, 5) # radius = 5
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