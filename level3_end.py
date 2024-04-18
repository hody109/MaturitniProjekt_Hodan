import subprocess
import pygame
import sys
import random
from settings import *
from main import Player

class Level3End:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.player = Player(self.screen)

        slide_width = 100
        slide_height = 20
        space_between_slides = 30  # Space between slides

        # Calculate the center of the screen horizontally
        center_x = screen_width // 2

        # Calculate the starting x position for the first slide to center them
        start_x = center_x - (1.5 * slide_width + space_between_slides)

        # Calculate the y position for the slides to be close to the bottom of the screen
        bottom_y = screen_height - slide_height - 20  # 20 pixels above the bottom edge of the screen

        self.slides = {
            'red': pygame.Rect(start_x, bottom_y, slide_width, slide_height),
            'blue': pygame.Rect(start_x + 2 * (slide_width + space_between_slides), bottom_y, slide_width, slide_height)
        }

        # Load background image
        self.background_image = pygame.image.load('assets/maps/map_end.png').convert()

        self.running = True
        pygame.mixer.music.load(r'assets/music/main_menu.mp3')
        pygame.mixer.music.play(-1)
        self.main_loop()

    def check_slide_collision(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
        for color, slide_rect in self.slides.items():
            if player_rect.colliderect(slide_rect):
                self.handle_slide_collision(color)

    def handle_slide_collision(self, color):
        if color == 'red':
            pygame.quit()
            subprocess.run(["python", "level0.py"])
            sys.exit()
        elif color == 'blue':
            pygame.quit()
            subprocess.run(["python", "outro.py"])
            sys.exit()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.running = False
                self.player.handle_event(event)

            # Draw background image
            self.screen.blit(self.background_image, (0, 0))

            self.player.update()
            self.player.draw()

            # Draw the slides
            for color, rect in self.slides.items():
                pygame.draw.rect(self.screen, pygame.Color(color), rect)

            self.check_slide_collision()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Level3End()