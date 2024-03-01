import  pygame
import sys
import random


# Nastavení velikosti okna
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))


# Unikove dveře
door_spawned = False
door_width = 80
door_height = 20
door_x, door_y = 0, 0  # Initial door position, to be set

# Nastavení barev
black = (0, 0, 0)
white = (255, 255, 255)
background = (51, 51, 0)
door_color = (96, 96, 96)

# Pozice a velikost hráče
player_size = 30
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 3
view_radius = 80  # Radius zorného pole pro hráče
player_movement = False

# Nastavení počátečního času a intervalu pro zastavení hudby
last_stop_time = pygame.time.get_ticks()
stop_interval = random.randint(10000, 20000)  # Náhodný čas mezi 10 a 20 sekundami

# Mince
coin_size = 15
num_coins = 5  # Počet mincí ve hře
coins = [(random.randint(0, screen_width - coin_size), random.randint(0, screen_height - coin_size)) for _ in range(num_coins)]

for _ in range(num_coins):
    coin_x = random.randint(0, screen_width - coin_size)
    coin_y = random.randint(0, screen_height - coin_size)
    coins.append((coin_x, coin_y))