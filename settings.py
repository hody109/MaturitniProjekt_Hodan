import pygame
import sys
import random
import subprocess
import os

pygame.init()

# Determine the base directory of the script to ensure correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Display settings
infoObject = pygame.display.Info()
screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Font settings
font_size = 15
font_path = os.path.join(BASE_DIR, 'assets', 'fonts', 'ScreamAgain.ttf')

# Door settings
door_spawned = False
door_width = 80
door_height = 80
door_x, door_y = 0, 0

# Color settings
black = (0, 0, 0)
white = (255, 255, 255)

# Load and scale background images correctly with absolute paths
background0 = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'maps', 'map0.png')).convert()
background0 = pygame.transform.scale(background0, (screen_width, screen_height))
background1 = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'maps', 'map1.png')).convert()
background1 = pygame.transform.scale(background1, (screen_width, screen_height))
background2 = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'maps', 'map2.png')).convert()
background2 = pygame.transform.scale(background2, (screen_width, screen_height))

door_color = (96, 96, 96)
COLOR_MAP = {
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'dark_green': (153, 255, 153),
    'dark_blue': (0, 0, 102),
    'yellow': (204, 204, 0)
}
color_sequence = ['blue', 'black', 'green', 'black', 'green', 'blue']  # Preset color sequence
tv_color = (200, 200, 200)
tv_position = (screen_width // 2 - 50, 50)  # Top middle of the screen for TV
tv_size = (200, 120)  # Size of the TV

# Player settings
player_speed = 3
chased_player_speed = 3.5
player_size = 30
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
view_radius = 100  # View radius for the player
player_movement = False

# Monster settings
monster_speed = 2
monster_size = 30

# Timing for game events
last_stop_time = pygame.time.get_ticks()
stop_interval = random.randint(10000, 20000)

# Coin settings
coin_size = 32
num_coins = 7
coins = [(random.randint(0, screen_width - coin_size), random.randint(0, screen_height - coin_size)) for _ in range(num_coins)]

for _ in range(num_coins):
    coin_x = random.randint(0, screen_width - coin_size)
    coin_y = random.randint(0, screen_height - coin_size)
    coins.append((coin_x, coin_y))