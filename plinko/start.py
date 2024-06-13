import pygame
import sys
import os
import json
from PIL import Image
import settings
from main import Game

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

USER_DATA_FILE = 'users.json'

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as file:
            json.dump({}, file)
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

user_data = load_user_data()

def create_account(username, password):
    if username in user_data:
        return False, "User already exists."
    user_data[username] = {'password': password, 'balance': 1000}
    save_user_data(user_data)
    return True, "Signed up."

def login(username, password):
    if username not in user_data:
        return False, "User not found."
    if user_data[username]['password'] != password:
        return False, "Invalid password."
    return True, "Logged in successfully."

def draw_text(screen, text, pos, font):
    screen_text = font.render(text, True, WHITE)
    text_rect = screen_text.get_rect(topleft=(pos[0], pos[1] + 200))
    screen.blit(screen_text, text_rect)

class Start:
    def __init__(self, gif_path):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH_START, settings.HEIGHT_START))
        pygame.display.set_caption('Plinko Game')
        self.clock = pygame.time.Clock()

        self.frames = self.load_gif_frames(gif_path)
        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_delay = 100  # ms between frames
        self.last_update_time = pygame.time.get_ticks()

        self.font = pygame.font.Font(None, 36)
        self.logged_in_user = None

    def load_gif_frames(self, gif_path):
        image = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = image.copy()
                frame = frame.convert('RGBA')
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()

                surface = pygame.image.fromstring(data, size, mode)
                frames.append(surface)
                image.seek(len(frames)) #next frame (gif)
        except EOFError:
            pass
        return frames

    def login_screen(self):
        running = True
        username = ""
        password = ""
        input_box_active = 'username'
        message = ""

        while running:
            self.update()
            self.draw()

            draw_text(self.screen, "Log in", (350, 50), self.font)
            draw_text(self.screen, "Username:", (200, 150), self.font)
            draw_text(self.screen, "Password:", (200, 200), self.font)

            #making windows bigger if text is too long
            username_width = self.font.size(username)[0]
            password_width = self.font.size('*' * len(password))[0]
            username_rect = pygame.Rect(350, 345, max(200, username_width + 10), 40)
            password_rect = pygame.Rect(350, 395, max(200, password_width + 10), 40)

            pygame.draw.rect(self.screen, WHITE, username_rect, 2)
            pygame.draw.rect(self.screen, WHITE, password_rect, 2)

            username_text = self.font.render(username, True, WHITE)
            password_text = self.font.render('*' * len(password), True, WHITE)
            self.screen.blit(username_text, (355, 350))
            self.screen.blit(password_text, (355, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        input_box_active = 'username'
                    elif password_rect.collidepoint(event.pos):
                        input_box_active = 'password'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        success, message = login(username, password)
                        if success:
                            self.logged_in_user = username
                            settings.USERNAME = self.logged_in_user
                            settings.BALANCE = user_data[username]['balance']
                            running = False
                            pygame.quit()
                            self.game = Game()
                            self.game.run()
                    elif event.key == pygame.K_TAB:
                        if input_box_active == 'username':
                            input_box_active = 'password'
                        else:
                            input_box_active = 'username'
                    elif event.key == pygame.K_BACKSPACE:
                        if input_box_active == 'username':
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    else:
                        if input_box_active == 'username':
                            username += event.unicode
                        else:
                            password += event.unicode

            draw_text(self.screen, message, (450, 350), self.font)
            pygame.display.flip()

    def register_screen(self):
        running = True
        username = ""
        password = ""
        input_box_active = 'username'
        message = ""

        while running:
            self.update()
            self.draw()

            draw_text(self.screen, "Sign Up", (350, 50), self.font)
            draw_text(self.screen, "Username:", (200, 150), self.font)
            draw_text(self.screen, "Password:", (200, 200), self.font)

            #making windows bigger if text is too long
            username_width = self.font.size(username)[0]
            password_width = self.font.size('*' * len(password))[0]
            username_rect = pygame.Rect(350, 345, max(200, username_width + 10), 40)
            password_rect = pygame.Rect(350, 395, max(200, password_width + 10), 40)

            pygame.draw.rect(self.screen, WHITE, username_rect, 2)
            pygame.draw.rect(self.screen, WHITE, password_rect, 2)

            username_text = self.font.render(username, True, WHITE)
            password_text = self.font.render('*' * len(password), True, WHITE)
            self.screen.blit(username_text, (355, 350))
            self.screen.blit(password_text, (355, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        input_box_active = 'username'
                    elif password_rect.collidepoint(event.pos):
                        input_box_active = 'password'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        success, message = create_account(username, password)
                        if success:
                            running = False
                    elif event.key == pygame.K_TAB:
                        if input_box_active == 'username':
                            input_box_active = 'password'
                        else:
                            input_box_active = 'username'
                    elif event.key == pygame.K_BACKSPACE:
                        if input_box_active == 'username':
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    else:
                        if input_box_active == 'username':
                            username += event.unicode
                        else:
                            password += event.unicode

            draw_text(self.screen, message, (450, 350), self.font)
            pygame.display.flip()

    def main_menu(self):
        running = True

        while running:
            self.update()
            self.draw()

            draw_text(self.screen, "1 - Log in", (350, 200), self.font)
            draw_text(self.screen, "2 - Sign up", (350, 250), self.font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.login_screen()
                        if self.logged_in_user:
                            running = False
                    if event.key == pygame.K_2:
                        self.register_screen()

            pygame.display.flip()

    def run(self):
        self.main_menu()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.last_update_time = current_time

    def draw(self):
        self.screen.fill(settings.BLACK)
        frame = self.frames[self.current_frame]
        frame_rect = frame.get_rect(center=(settings.WIDTH_START // 2, 150))
        self.screen.blit(frame, frame_rect)



if __name__ == '__main__':
    gif_path = "graphics/logo.gif"
    viewer = Start(gif_path)
    viewer.run()
