import pygame
import sys
import random
import subprocess
from settings import *


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mixer.init()
balloon_pop_sound = pygame.mixer.Sound(r'assets/sounds/balloon-pop.mp3')


class Balloon:
    def __init__(self, color, position):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], 20, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_MAP[self.color], self.rect)

class TV:
    def __init__(self, position, size):
        self.width = 200
        self.height = 100
        self.x = (screen_width - self.width) // 2
        self.y = 30
        self.position = (self.x, self.y)
        self.size = (self.width, self.height)
        self.color = 'white'
        self.show_color_time = pygame.time.get_ticks()



    def draw(self, screen):
        color = COLOR_MAP.get(self.color, (255, 255, 255))  # Výchozí bílá, pokud barva není definována
        pygame.draw.rect(screen, color, (*self.position, *self.size))

    def show_color(self, color, current_time):
        self.color = color
        self.show_color_time = current_time

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = 0.3
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.size = player_size

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

            # Omezení pohybu hráče na herní plochu
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

    def draw(self):
        pygame.draw.rect(self.screen, white, (self.rect.x, self.rect.y, self.size, self.size))



class Game:
    def __init__(self):
        self.screen = screen
        self.player = Player(self.screen)
        self.balloons = [Balloon(random.choice(['green', 'blue', 'black']), (random.randint(0, screen_width-20), random.randint(0, screen_height-20))) for _ in range(12)]
        self.tv = TV((100, 100), (100, 50))
        self.running = True
        self.color_sequence = ['blue', 'black', 'green', 'black', 'green', 'blue']
        #todo: Obcas se nespawnuji vsechny barvy - zpravit asap
        self.sequence_index = 0
        self.show_next_color(pygame.time.get_ticks())

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.check_balloon_collisions()

    def draw(self):
        self.screen.fill(background1)
        self.player.draw()
        for balloon in self.balloons:
            balloon.draw(self.screen)
        self.tv.draw(self.screen)
        pygame.display.flip()

    def check_balloon_collisions(self):
        player_rect = self.player.rect
        for balloon in self.balloons:
            if player_rect.colliderect(balloon.rect):
                if balloon.color == self.color_sequence[self.sequence_index]:
                    self.balloons.remove(balloon)
                    balloon_pop_sound.play()
                    self.sequence_index += 1
                    if self.sequence_index < len(self.color_sequence):
                        self.show_next_color(pygame.time.get_ticks())
                    else:
                        print("You've matched all the colors!")
                        self.running = False
                else:
                    self.trigger_jumpscare()
                break

    def show_next_color(self, current_time):
        next_color = self.color_sequence[self.sequence_index]
        self.tv.show_color(next_color, current_time)

    def trigger_jumpscare(self):
        print("Wrong balloon! Game Over.")
        self.running = False
        #todo: Logika pro jumpscare

if __name__ == "__main__":
    game = Game()
    game.main_loop()
