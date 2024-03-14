import pygame
from settings import screen_width, screen_height

class Level0:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('path/to/level0/background.png').convert()

    def draw(self):
        self.screen.blit(self.background, (0, 0))