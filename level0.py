import subprocess
import pygame
import sys
import random
from settings import *
from main import Player
import os

class level0:
    """
    Represents the first level of the game, handling the game mechanics like player movement,
    collecting coins, encountering doors, and managing music and jum scares.
    """
    def __init__(self):
        """
        Initializes the level with setting up the game environment and starting the game loop.
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.jumpscare_manager = JumpscareManager(self.screen)
        self.player = Player(self.screen)
        self.door = Door(self.screen)
        self.coins = [self.generate_coin_position() for _ in range(num_coins)]
        self.total_coins = len(self.coins)
        self.collected_coins = 0
        self.font = pygame.font.Font(font_path, font_size)
        self.door_spawned = False
        self.running = True
        pygame.display.set_caption("Level 0 - The Lobby")
        self.start_time = pygame.time.get_ticks()
        self.show_message = True
        self.message_duration = 5000
        self.initial_message = "What.... What is this place? How did i get here?!"
        self.message_font = pygame.font.Font(font_path, font_size)
        self.coin_image = pygame.image.load('assets/tiles/coin.png').convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (coin_size, coin_size))
        self.main_loop()
        pygame.time.Clock().tick(60)

    def generate_coin_position(self):
        """
            Generates a random position within the screen boundaries for a coin.
            :return: A tuple containing the x and y coordinates of the coin.
            :rtype: tuple
            """
        return (random.randint(0, screen_width - coin_size), random.randint(0, screen_height - coin_size))

    def check_coin_collision(self):
        """
        Checks for collisions between the player and coins, updates coin collection and handles door spawning.
        """
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
        for coin in self.coins[:]:
            coin_rect = pygame.Rect(coin[0], coin[1], coin_size, coin_size)
            if player_rect.colliderect(coin_rect):
                self.coins.remove(coin)
                self.collected_coins += 1
                self.music_manager.pickup_sound.play()
            if not self.coins:
                self.door_spawned = True
                self.door.x, self.door.y = self.door.generate_random_door_position()

    def main_loop(self):
        """
        The main game loop handling events, updates, and rendering.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.Clock().tick(60)
        self.quit()

    def handle_events(self):
        """
        Handles user input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)

    def update(self):
        """
        Updates the game state, including checking collisions and managing time-dependent events.
        """
        current_time = pygame.time.get_ticks()
        player_moving = self.player.is_moving()
        music_playing = pygame.mixer.music.get_busy()

        self.player.update()
        self.music_manager.update()
        self.jumpscare_manager.update(music_playing, player_moving, current_time)
        self.check_coin_collision()

        if current_time - self.start_time > self.message_duration:
            self.show_message = False

        if self.door_spawned:
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
            door_rect = pygame.Rect(self.door.x, self.door.y, door_width, door_height)
            if player_rect.colliderect(door_rect):
                self.change_level()

    def render(self):
        """
        Renders the game frame, drawing all game elements on the screen.
        """
        self.screen.blit(background0, (0, 0))
        self.player.draw()
        if self.door_spawned:
            self.door.draw()
        for coin in self.coins:
            self.screen.blit(self.coin_image, (coin[0], coin[1]))

        mask = pygame.Surface((screen_width, screen_height))
        mask.fill((0, 0, 0))

        player_center_x = self.player.x
        player_center_y = self.player.y

        pygame.draw.circle(mask, (255, 255, 255), (player_center_x, player_center_y), view_radius)
        mask.set_colorkey((255, 255, 255))
        self.screen.blit(mask, (0, 0))

        if self.show_message:
            message_surface = self.message_font.render(self.initial_message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(screen_width / 2, 20))
            self.screen.blit(message_surface, message_rect)

        coins_text = f"{self.collected_coins} / {self.total_coins}"
        text_surf = self.font.render(coins_text, True, white)
        self.screen.blit(text_surf, (screen_width - text_surf.get_width() - 10, 10))

        if len(self.coins) == 0:
            exit_message = "Great, now look for the exit"
            message_surf = self.font.render(exit_message, True, white)
            message_rect = message_surf.get_rect(center=(screen_width / 2, 20))
            self.screen.blit(message_surf, message_rect)
        pygame.display.flip()

    def change_level(self):
        """
        Handles the transition to the next level of the game.
        """
        pygame.quit()
        subprocess.run(["python", "level1.py"])
        sys.exit()

    def quit(self):
        """
        Quits the game and closes the application.
        """
        pygame.quit()
        sys.exit()

class MusicManager:
    """
    Manages background music and sound effects for the game.
    """
    def __init__(self):
        """
        Initializes the music manager, loads music and sound effects.
        """
        pygame.mixer.music.load(r'assets/music/music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.door_spawn = pygame.mixer.Sound(r'assets/sounds/door_spawn.mp3')
        self.stop_sound = pygame.mixer.Sound(r'assets/music/music-stop.mp3')
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.pickup_sound = pygame.mixer.Sound(r'assets/sounds/pickup.mp3')
        self.last_stop_time = pygame.time.get_ticks()
        self.stop_interval = random.randint(10000, 20000)
        self.music_playing = True

    def update(self):
        """
        Updates the state of music playback based on game events.
        """
        current_time = pygame.time.get_ticks()
        if self.music_playing and current_time - self.last_stop_time > self.stop_interval:
            pygame.mixer.music.stop()
            self.stop_sound.play()
            self.music_playing = False
            self.last_stop_time = current_time
            self.stop_interval = random.randint(3000, 7000)
        elif not self.music_playing and current_time - self.last_stop_time > self.stop_interval:
            pygame.mixer.music.play(-1)
            self.music_playing = True
            self.last_stop_time = current_time
            self.stop_interval = random.randint(10000, 20000)

class JumpscareManager:
    """
    Manages the triggering of jumpscares based on game conditions.
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

    def update(self, music_playing, player_moving, current_time):
        """
        Updates the jumpscare conditions.
        """
        if not music_playing and self.music_stopped_time is None:
            self.music_stopped_time = current_time
        elif music_playing:
            self.music_stopped_time = None

        if self.music_stopped_time and player_moving and current_time - self.music_stopped_time > 1000 and not self.jumpscare_triggered:
            self.trigger_jumpscare()

    def trigger_jumpscare(self):
        """
        Triggers a jumpscare event.
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

class Door:
    """
    Represents a door in the game, handling its appearance and interaction.
    """
    def __init__(self, screen):
        """
        Initializes the door with its position and loads its image.
        :param screen: The main game screen.
        :type screen: pygame.Surface
        """
        self.door_spawn = pygame.mixer.Sound(r'assets/sounds/door_spawn.mp3')
        self.door_spawned = True
        self.screen = screen
        self.x, self.y = self.generate_random_door_position()
        self.image = pygame.image.load('assets/tiles/exit_door.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))

    def generate_random_door_position(self):
        """
        Generates a random position for the door based on predefined screen edges.
        :return: A tuple of x and y coordinates for the door.
        :rtype: tuple
        """
        edge = random.choice(["top", "bottom", "left", "right"])
        self.door_spawn.play()
        if edge == "top":
            return random.randint(0, screen_width - 50), 0
        elif edge == "bottom":
            return random.randint(0, screen_width - 50), screen_height - 100
        elif edge == "left":
            return 0, random.randint(0, screen_height - 100)
        else:  # edge == "right"
            return screen_width - 50, random.randint(0, screen_height - 100)

    def draw(self):
        """
        Draws the door on the screen at its current position.
        """
        if self.door_spawned:
            self.screen.blit(self.image, (self.x, self.y))



if __name__ == "__main__":
    level0()
