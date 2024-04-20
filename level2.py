from settings import *
from main import Player
from main import NPC
import os

class Computer:
    """
    Represents a computer within the game level that can interact with the player through a question-answer interface.
    """
    def __init__(self, screen, x, y):
        """
        Initializes the computer with its position and loads the necessary image.

        :param screen: The game screen where the computer will be displayed.
        :param x: The x-coordinate of the computer's position.
        :param y: The y-coordinate of the computer's position.
        :type screen: pygame.Surface
        :type x: int
        :type y: int
                """
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(r'assets/tiles/computer.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.font = pygame.font.Font(None, 48)
        self.question = "What am I? :"
        self.active = False
        self.answer = ""
        self.show_input = False
        self.computer_sound = pygame.mixer.Sound(r'assets/sounds/computer.mp3')

    def draw(self):
        """
        Draws the computer on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def check_answer(self, answer):
        """
        Checks the player's answer and determines if it is correct, leading to level progression or other outcomes.

        :param answer: The player's input answer.
        :type answer: str
        """
        if answer.lower() == "balloon":
            pygame.quit()
            subprocess.run(["python", "level3_end.py"])
            sys.exit()


class level2:
    """
    The second level of the game featuring interactions with NPCs, a computer, and various other interactive objects.
    """
    def __init__(self):
        """
        Initializes level 2, setting up the environment and starting the main game loop.
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.start_time = pygame.time.get_ticks()
        self.jumpscare_manager = JumpscareManager(self.screen)
        self.player = Player(self.screen)
        self.font = pygame.font.Font(font_path, font_size)
        self.door_spawned = False
        pygame.display.set_caption("Level 2 - The Hub")
        self.running = True
        self.npc = NPC(self.screen, self.player)
        self.font = pygame.font.Font(font_path, font_size)
        self.table = InteractiveObject(self.screen, screen_width // 2, screen_height // 2, 150, 100)
        self.computer = Computer(self.screen, screen_width - 50, screen_height // 2)
        self.countdown_started = False
        self.countdown_time = 35
        self.countdown_start_ticks = None
        self.view_radius = 200  # Radius zorného pole pro hráče
        self.main_loop()

    def main_loop(self):
        """
        Main game loop that handles event processing, game state updates, and rendering.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.Clock().tick(60)
        self.quit()

    def handle_events(self):
        """
        Handles all player input events and triggers corresponding game logic.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.computer.rect.colliderect(self.player.rect):
                        self.computer.active = True
                        self.computer.show_input = True
                        self.computer.computer_sound.play()
                elif self.computer.show_input:
                    if event.key == pygame.K_RETURN:
                        self.computer.check_answer(self.computer.answer)
                        self.computer.answer = ""
                        self.computer.show_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.computer.answer = self.computer.answer[:-1]
                    else:
                        self.computer.answer += event.unicode

    def update(self):
        """
        Updates the game state, including player, NPC, and other interactive elements.
        """
        self.npc.update()
        self.player.update()
        self.player.is_moving()

        if self.door_spawned:
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
            door_rect = pygame.Rect(self.door.x, self.door.y, door_width, door_height)
            if player_rect.colliderect(door_rect):
                # Přechod do dalšího levelu
                self.change_level()
        if self.table.rect.colliderect(self.player.rect) and self.player.interact:
            if not self.countdown_started:
                self.countdown_started = True
                self.countdown_start_ticks = pygame.time.get_ticks()
                self.table.show_question = True
            self.table.play_sound()

        if self.countdown_started:
            elapsed_time = (pygame.time.get_ticks() - self.countdown_start_ticks) // 1000
            self.countdown_time = max(0, 60 - elapsed_time)  # Aby čas nepoklesl pod nulu

        if self.countdown_time == 0:
            self.npc.expand_vision(2000)  # Rozšíření vision radius na 2000

        if self.table.show_question:
            riddle_text = "I can rise without wings, and make smiles bright as bay. With vibrant colors on display, catch me, before i float away"
            text_surface = self.font.render(riddle_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50))
            self.screen.blit(text_surface, text_rect)

    def render(self):
        """
        Renders all game elements to the screen.
        """
        self.screen.blit(background2, (0, 0))
        self.player.draw()
        self.npc.draw()
        self.table.draw()
        self.computer.draw()

        mask = pygame.Surface((screen_width, screen_height))
        mask.fill((0, 0, 0))

        player_center_x = self.player.x
        player_center_y = self.player.y

        pygame.draw.circle(mask, (255, 255, 255), (player_center_x, player_center_y), self.view_radius)
        mask.set_colorkey((255, 255, 255))
        self.screen.blit(mask, (0, 0))

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= 5000:  # Zobraz text, pokud uplynulo méně než 5 sekund
            text_surf = self.font.render("I don't think I'm alone here...", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(screen_width // 2, 20))
            self.screen.blit(text_surf, text_rect)
        if self.countdown_started:
            countdown_text = self.font.render(f'{self.countdown_time}s', True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(topright=(screen_width - 20, 20))
            self.screen.blit(countdown_text, countdown_rect)
        if self.computer.active and self.computer.show_input:
            question_surface = self.font.render(self.computer.question, True, (255, 255, 255))
            question_rect = question_surface.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
            self.screen.blit(question_surface, question_rect)
            answer_surface = self.font.render(self.computer.answer, True, (255, 255, 255))
            answer_rect = answer_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(answer_surface, answer_rect)
        pygame.display.flip()

    def change_level(self):
        """
        Handles the transition to the next level of the game.
        """
        pygame.quit()
        subprocess.run(["python", "level3_end.py"])
        sys.exit()

    def quit(self):
        """
        Quits the game and exits the program.
        """
        pygame.quit()
        sys.exit()

class InteractiveObject:
    """
    Represents interactive objects within the game that can respond to player actions.
    """
    def __init__(self, screen, x, y, width, height):
        """
        Initializes an interactive object with its position and dimensions.

        :param screen: The game screen where the object will be displayed.
        :param x: The x-coordinate of the object's position.
        :param y: The y-coordinate of the object's position.
        :param width: The width of the object.
        :param height: The height of the object.
        :type screen: pygame.Surface
        :type x: int
        :type y: int
        :type width: int
        :type height: int
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(r'assets/tiles/table.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 75))
        self.rect = self.image.get_rect(center=(x, y))
        self.interact_sound = pygame.mixer.Sound(r'assets/sounds/hadanka.wav')
        self.show_question = False
        self.question_time = 0

    def draw(self):
        """
        Draws the interactive object on the screen.
        """
        self.screen.blit(self.image, self.rect)
    def play_sound(self):
        """
        Plays a sound associated with interaction with the object.
        """
        self.interact_sound.play()
        self.show_question = True
        self.question_time = pygame.time.get_ticks()

    def update(self):
        """
        Updates the state of InterActive object
        """
        if self.show_question:
            current_time = pygame.time.get_ticks()
            if current_time - self.question_time > 60000:
                self.show_question = False


class MusicManager:
    """
    Manages background music and sound effects for the level.
    """
    def __init__(self):
        """
        Initializes the music manager and starts playing the background music.
        """
        pygame.mixer.music.load(r'assets/music/level2.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.stop_sound = pygame.mixer.Sound(r'assets/music/music-stop.mp3')
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.pickup_sound = pygame.mixer.Sound(r'assets/sounds/pickup.mp3')
        self.music_playing = True

class JumpscareManager:
    """
    Manages jumpscare triggers based on certain game conditions.
    """
    def __init__(self, screen):
        """
        Initializes the jumpscare manager with references to the game screen.

        :param screen: The main game screen.
        :type screen: pygame.Surface
        """
        self.screen = screen
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.jumpscare_triggered = False
        self.music_stopped_time = None


    def trigger_jumpscare(self):
        """
        Triggers a jumpscare effect visually and audibly.
        """
        self.jumpscare_sound.play()
        self.screen.blit(self.jumpscare_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        subprocess.run(["python", "menu.py"])
        sys.exit()

if __name__ == "__main__":
    level2()