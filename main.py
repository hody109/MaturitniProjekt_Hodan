from menu import MainMenu
import pygame
from settings import *
from level2 import  JumpscareManager
class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x = 10
        self.y = 10
        self.speed = player_speed
        self.size = player_size
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        # Klávesy nejsou v této verzi přímo používány, ale mohou být ponechány pro další použití
        self.keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.move_right = True
            elif event.key == pygame.K_UP:
                self.move_up = True
            elif event.key == pygame.K_DOWN:
                self.move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False
            elif event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False

    def is_moving(self):
        return self.move_left or self.move_right or self.move_up or self.move_down

    def update(self):
        if self.move_left:
            self.x -= self.speed
        if self.move_right:
            self.x += self.speed
        if self.move_up:
            self.y -= self.speed
        if self.move_down:
            self.y += self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        # Omezení pohybu hráče na herní plochu
        self.rect.x = max(0, min(self.rect.x, screen_width - self.size))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.size))

    def draw(self):
        pygame.draw.rect(self.screen, white, (self.rect.x, self.rect.y, self.size, self.size))


class NPC:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = 2
        self.chase_speed = 2.6
        self.size = 30
        self.vision_radius = 150
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = (255, 0, 0)  # Červená barva pro NPC
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.distance_moved = 0
        self.move_distance_limit = random.randint(50, 150)  # Náhodně zvolená vzdálenost pro změnu směru
        self.chase_sound = pygame.mixer.Sound(r'assets/sounds/skin_stealer.mp3')
        self.is_chasing = False

    def move_randomly(self):
        if self.distance_moved >= self.move_distance_limit:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.distance_moved = 0
            self.move_distance_limit = random.randint(50, 150)  # Reset limitu vzdálenosti

        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed

        self.distance_moved += self.speed  # Aktualizace ušlé vzdálenosti

        # Udržení NPC na obrazovce
        self.x = max(0, min(self.x, screen_width - self.size))
        self.y = max(0, min(self.y, screen_height - self.size))

    def chase_player(self):
        self.chase_sound.play()
        self.chase_sound.set_volume(0.5)
        self.is_chasing = True
        if self.x < self.player.x:
            self.x += self.chase_speed
        elif self.x > self.player.x:
            self.x -= self.chase_speed

        if self.y < self.player.y:
            self.y += self.chase_speed
        elif self.y > self.player.y:
            self.y -= self.chase_speed

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

        # Detekce, zda je hráč v zorném poli
        if pygame.math.Vector2(self.x - self.player.x, self.y - self.player.y).length() < self.vision_radius:
            self.chase_player()
        else:
            self.move_randomly()

        # Detekce kolize s hráčem
        # todo: dodelat kolizi s hracem
        #if self.rect.colliderect(self.player.rect):


    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Vykreslení zorného pole pro vizuální debug
        pygame.draw.circle(self.screen, (0, 255, 0), (self.x + self.size // 2, self.y + self.size // 2), self.vision_radius, 1)



if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu()