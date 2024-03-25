import  pygame
import sys
import random

pygame.init()
# Nastavení velikosti okna
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

font_size = 30
font_path = r'assets/fonts/CustomFont.ttf'


# Unikove dveře
door_spawned = False
door_width = 80
door_height = 80
door_x, door_y = 0, 0  # Initial door position, to be set

# Nastavení barev
black = (0, 0, 0)
white = (255, 255, 255)
background0 = pygame.image.load('assets/maps/map0.png').convert()
background0 = pygame.transform.scale(background0, (screen_width, screen_height))
background1 = pygame.image.load('assets/maps/map1.png').convert()
background1 = pygame.transform.scale(background1, (screen_width, screen_height))
background2 = (102, 51, 0)
background3 = (51, 51, 0)
door_color = (96, 96, 96)
COLOR_MAP = {
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'dark_green': (153, 255, 153),
    'dark_blue': (0, 0, 102),
    'yellow': (204, 204, 0)
}
color_sequence = ['blue', 'black', 'green', 'black', 'green', 'blue']  # Pevně dané pořadí barev
tv_color = (200, 200, 200)
tv_position = (screen_width // 2 - 50, 50)  # Televize na horní straně uprostřed
tv_size = (200, 120)  # Velikost televize

# Pozice a velikost hráče
player_size = 30
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
view_radius = 80  # Radius zorného pole pro hráče
player_movement = False

# Nastavení počátečního času a intervalu pro zastavení hudby
last_stop_time = pygame.time.get_ticks()
stop_interval = random.randint(10000, 20000)  # Náhodný čas mezi 10 a 20 sekundami

# Mince
coin_size = 15
num_coins = 10  # Počet mincí ve hře
coins = [(random.randint(0, screen_width - coin_size), random.randint(0, screen_height - coin_size)) for _ in range(num_coins)]


for _ in range(num_coins):
    coin_x = random.randint(0, screen_width - coin_size)
    coin_y = random.randint(0, screen_height - coin_size)
    coins.append((coin_x, coin_y))