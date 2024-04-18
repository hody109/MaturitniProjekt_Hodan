from settings import *
from main import Player
import os

class level1:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.jumpscare_manager = JumpscareManager(self.screen)
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
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.Clock().tick(60)
        self.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pop_balloon()
            self.player.handle_event(event)

    def change_level(self):
        pygame.quit()
        subprocess.run(["python", "level2.py"])

    def pop_balloon(self):
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
        colors = ['blue', 'green', 'black', 'dark-green', 'yellow', 'light-blue']
        return [Balloon(self.screen, random.choice(colors)) for _ in range(20)]


    def update(self):
        self.player.update()

    def render(self):
        self.screen.blit(background1, (0, 0))
        self.television.draw()

        self.player.draw()
        for balloon in self.balloons:
            balloon.draw()
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def quit(self):
        pygame.quit()
        sys.exit()

class Balloon:
    def __init__(self, screen, color):
        self.screen = screen
        self.color = color
        original_image = pygame.image.load(f'assets/tiles/{color}_balloon.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * 2), int(original_image.get_height() * 2)))
        self.rect = self.image.get_rect(center=(random.randint(self.image.get_width() // 2, screen_width - self.image.get_width() // 2),
                                               random.randint(self.image.get_height() // 2, screen_height - self.image.get_height() // 2)))

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Television:
    def __init__(self, screen, initial_color):
        self.screen = screen
        self.color = initial_color
        self.width = 200
        self.height = 100
        self.rect = pygame.Rect(screen_width // 2 - self.width // 2, 10, self.width, self.height)

    def update(self, new_color):
        self.color = new_color

    def draw(self):
        pygame.draw.rect(self.screen, pygame.Color(self.color), self.rect)
class MusicManager:
    def __init__(self):
        pygame.mixer.music.load(r'assets/music/level1.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.door_spawn = pygame.mixer.Sound(r'assets/sounds/door_spawn.mp3')
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.music_playing = True


class JumpscareManager:
    def __init__(self, screen):
        self.screen = screen
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.jumpscare_triggered = False

    def trigger_jumpscare(self):
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
