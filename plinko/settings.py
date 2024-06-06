import ctypes, pygame, pymunk


TITLE_STRING = 'Plinkooo'
FPS = 60

ctypes.windll.user32.SetProcessDPIAware()

WIDTH = 1920
HEIGHT = 1080

BG_COLOR = (16, 32, 45)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
COLOR = WHITE
ACTIVE = False
BET_TEXT = '0'
COLOR_AUTO = LIGHT_BLUE
AUTO = 0
AUTO_TEXT = '0'
ACTIVE_AUTO = False


MULTI_HEIGHT = int(HEIGHT / 19) # 56
MULTI_COLLISION = HEIGHT - (MULTI_HEIGHT * 2) # 968

SCORE_RECT = int(WIDTH / 16) # 120

OBSTACLE_COLOR = "White"
OBSTACLE_RAD = int(WIDTH / 240) # 8
OBSTACLE_PAD = int(HEIGHT / 19) # 56
OBSTACLE_START = (int((WIDTH / 2) - OBSTACLE_PAD), int((HEIGHT - (HEIGHT * .9)))) # (904, 108)
segmentA_2 = OBSTACLE_START

BALL_RAD = 16

RISK = 0
BALANCE = 1000.00
BET = float(BET_TEXT)
AUTO = int(AUTO_TEXT)
BALLS = 0
balance_log = [BALANCE]
enough_balance = True

multipliers = {
    "1000": 0,
    "130": 0,
    "110": 0,
    "41": 0,                            
    "26": 0,
    "16": 0,
    "10": 0,                           
    "9": 0,
    "5": 0,
    "4": 0,
    "3": 0,
    "2": 0,
    "1.5": 0,
    "1.4": 0,
    "1.2": 0,
    "1.1": 0,
    "1": 0,
    "0.5": 0,
    "0.3": 0,
    "0.2": 0
    }

    # RGB Values for multipliers
multi_rgb = {
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

NUM_MULTIS = 17

BALL_CATEGORY = 1
OBSTACLE_CATEGORY = 2
BALL_MASK = pymunk.ShapeFilter.ALL_MASKS() ^ BALL_CATEGORY
OBSTACLE_MASK = pymunk.ShapeFilter.ALL_MASKS()

pygame.mixer.init()
click = pygame.mixer.Sound("audio/click.mp3")
click.set_volume(1)
sound01 = pygame.mixer.Sound("audio/001.mp3")
sound01.set_volume(0.2)
sound02 = pygame.mixer.Sound("audio/002.mp3")
sound02.set_volume(0.3)
sound03 = pygame.mixer.Sound("audio/003.mp3")
sound03.set_volume(0.4)
sound04 = pygame.mixer.Sound("audio/004.mp3")
sound04.set_volume(0.5)
sound05 = pygame.mixer.Sound("audio/005.mp3")
sound05.set_volume(0.6)
sound06 = pygame.mixer.Sound("audio/006.mp3")
sound06.set_volume(0.7)
sound07 = pygame.mixer.Sound("audio/007.mp3")
sound07.set_volume(0.8)

