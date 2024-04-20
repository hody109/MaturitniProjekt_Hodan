from settings import *
from main import Player
import os

class Level3End:
    """
    Represents the end of levels where the player chooses between two different slides, leading to different outcomes.
    """
    def __init__(self):
        """
        Initializes the end level environment, sets up the player, slides, and starts the main game loop.
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen = screen
        self.player = Player(self.screen)
        slide_width = 100
        slide_height = 20
        pygame.display.set_caption("Level 3 - The End")
        space_between_slides = 30
        center_x = screen_width // 2
        start_x = center_x - (1.5 * slide_width + space_between_slides)
        bottom_y = screen_height - slide_height - 20

        self.slides = {
            'red': pygame.Rect(start_x, bottom_y, slide_width, slide_height),
            'blue': pygame.Rect(start_x + 2 * (slide_width + space_between_slides), bottom_y, slide_width, slide_height)
        }
        self.background_image = pygame.image.load('assets/maps/map_end.png').convert()
        self.running = True
        pygame.mixer.music.load(r'assets/music/end.mp3')
        pygame.mixer.music.play(-1)
        self.main_loop()

    def check_slide_collision(self):
        """
        Checks for collisions between the player and the slides.
        """
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
        for color, slide_rect in self.slides.items():
            if player_rect.colliderect(slide_rect):
                self.handle_slide_collision(color)

    def handle_slide_collision(self, color):
        """
        Handles the events that occur when the player collides with a slide.

        :param color: The color of the slide which identifies the slide.
        :type color: str
        """
        if color == 'red':
            pygame.mixer.music.stop()
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.quit()
            subprocess.run(["python", "level0.py"])
            sys.exit()
        elif color == 'blue':
            pygame.mixer.music.stop()
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.quit()
            subprocess.run(["python", "outro.py"])
            sys.exit()

    def main_loop(self):
        """
        Main game loop for level end, handles events, updates, and rendering.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.running = False
                self.player.handle_event(event)

            self.screen.blit(self.background_image, (0, 0))
            self.player.update()
            self.player.draw()
            self.player.is_moving()

            for color, rect in self.slides.items():
                pygame.draw.rect(self.screen, pygame.Color(color), rect)

            self.check_slide_collision()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Level3End()