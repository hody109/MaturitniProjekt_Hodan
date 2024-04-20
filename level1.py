from settings import *
from main import Player
import os

class level1:
    """
    Represents the second level of the game where players interact with balloons and a color sequence
    displayed on a television. Correct interactions lead to level progression, while errors may trigger
    jumpscares.
    """
    def __init__(self):
        """
        Initializes the level with game settings and starts the main game loop.
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.jumpscare_manager = JumpscareManager(self.screen)
        pygame.display.set_caption("Level 1 - Fun")
        self.player = Player(self.screen)
        self.balloons = self.spawn_balloons()
        self.color_sequence = ['blue', 'black', 'green', 'black', 'blue', 'green']
        self.current_color_index = 0
        self.balloons_popped = 0
        self.television = Television(self.screen, self.color_sequence[self.current_color_index])
        self.balloon_pop_sound = pygame.mixer.Sound(r'assets/sounds/balloon-pop.mp3')
        self.electricity = pygame.mixer.Sound(r'assets/sounds/eletricity.wav')
        self.running = True
        self.main_loop()

    def main_loop(self):
        """
        Main game loop for level1, handling events, updates, and rendering.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.Clock().tick(60)
        self.quit()

    def handle_events(self):
        """
        Handles user input events, including balloon popping and player movement.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pop_balloon()
            self.player.handle_event(event)

    def change_level(self):
        """
        Changes to the next level of the game upon successful completion.
        """
        pygame.quit()
        subprocess.run(["python", "level2.py"])

    def pop_balloon(self):
        """
        Checks for collisions between player and balloons and handles game logic for balloon popping.
        """
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
        for balloon in self.balloons[:]:
            if player_rect.colliderect(balloon.rect):
                if balloon.color == self.color_sequence[self.current_color_index]:
                    self.balloons.remove(balloon)
                    self.balloon_pop_sound.play()
                    self.balloons_popped += 1
                    self.current_color_index = (self.current_color_index + 1) % len(self.color_sequence)
                    self.television.update(self.color_sequence[self.current_color_index])
                    if self.balloons_popped == len(self.color_sequence):
                        self.electricity.play()
                        pygame.mixer.music.stop()
                        self.screen.fill((0, 0, 0))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        self.change_level()
                else:
                    self.electricity.play()
                    pygame.mixer.music.stop()
                    self.screen.fill((0, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    self.jumpscare_manager.trigger_jumpscare()
    def spawn_balloons(self):
        """
        Creates a list of balloon objects at random positions on the screen.

        :return: List of balloon objects.
        :rtype: list
        """
        colors = ['blue', 'green', 'black', 'dark-green', 'yellow', 'light-blue']
        return [Balloon(self.screen, random.choice(colors)) for _ in range(20)]


    def update(self):
        """
        Updates the game state, including player and game object movements.
        """
        self.player.update()
        self.player.is_moving()

    def render(self):
        """
        Renders all game elements to the screen.
        """
        self.screen.blit(background1, (0, 0))
        self.television.draw()

        self.player.draw()
        for balloon in self.balloons:
            balloon.draw()
        pygame.display.flip()

    def quit(self):
        """
        Quits the game and exits the program.
        """
        pygame.quit()
        sys.exit()

class Balloon:
    """
    Represents a balloon in the game, which can be popped by the player.
    """
    def __init__(self, screen, color):
        """
        Initializes a balloon with a color and random position.

        :param screen: The game screen.
        :param color: Color of the balloon.
        :type screen: pygame.Surface
        :type color: str
                """
        self.screen = screen
        self.color = color
        original_image = pygame.image.load(f'assets/tiles/{color}_balloon.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * 2), int(original_image.get_height() * 2)))
        self.rect = self.image.get_rect(center=(random.randint(self.image.get_width() // 2, screen_width - self.image.get_width() // 2),
                                               random.randint(self.image.get_height() // 2, screen_height - self.image.get_height() // 2)))

    def draw(self):
        """
        Draws the balloon on the game screen.
        """
        self.screen.blit(self.image, self.rect)

class Television:
    """
    Represents a television that displays the current target color for the player to interact with.
    """
    def __init__(self, screen, initial_color):
        """
        Initializes the television with a starting color.

        :param screen: The game screen where the television is displayed.
        :param initial_color: The initial color displayed on the television.
        :type screen: pygame.Surface
        :type initial_color: str
        """
        self.screen = screen
        self.color = initial_color
        self.width = 200
        self.height = 100
        self.rect = pygame.Rect(screen_width // 2 - self.width // 2, 10, self.width, self.height)

    def update(self, new_color):
        """
        Updates the color displayed on the television.

        :param new_color: The new color to display.
        :type new_color: str
        """
        self.color = new_color

    def draw(self):
        """
        Draws the television on the screen.
        """
        pygame.draw.rect(self.screen, pygame.Color(self.color), self.rect)

class MusicManager:
    """
    Manages background music and ambient sounds for the level.
    """
    def __init__(self):
        """
        Initializes the music manager and starts playing level music.
        """
        pygame.mixer.music.load(r'assets/music/level1.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.door_spawn = pygame.mixer.Sound(r'assets/sounds/door_spawn.mp3')
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.music_playing = True


class JumpscareManager:
    """
    Manages jumpscares in response to player errors or specific game events.
    """
    def __init__(self, screen):
        """
        Initializes the jumpscare manager with the game screen.

        :param screen: The main game screen.
        :type screen: pygame.Surface
        """
        self.screen = screen
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.jumpscare_triggered = False

    def trigger_jumpscare(self):
        """
        Triggers a jumpscare effect on the screen.
        """
        self.screen.fill((0, 0, 0))
        self.jumpscare_sound.play()
        self.screen.blit(self.jumpscare_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)
        self.jumpscare_triggered = False
        self.music_stopped_time = None
        pygame.quit()
        subprocess.run(["python", "menu.py"])

if __name__ == "__main__":
    level1()
