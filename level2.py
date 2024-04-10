import subprocess
import pygame
import sys
import random
from settings import *
from main import Player
from main import NPC


class level2:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.start_time = pygame.time.get_ticks()
        self.jumpscare_manager = JumpscareManager(self.screen)
        self.player = Player(self.screen)
        self.door = Door(self.screen)
        self.font = pygame.font.Font(font_path, font_size)
        self.door_spawned = False
        self.running = True
        self.npc = NPC(self.screen, self.player)  # Předání instance hráče do NPC
        self.font = pygame.font.Font(font_path, font_size)
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
            self.player.handle_event(event)

    def update(self):
        current_time = pygame.time.get_ticks()
        player_moving = self.player.is_moving()
        music_playing = pygame.mixer.music.get_busy()
        self.npc.update()

        self.player.update()
        self.music_manager.update()

        if self.door_spawned:
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
            door_rect = pygame.Rect(self.door.x, self.door.y, door_width, door_height)
            if player_rect.colliderect(door_rect):
                # Přechod do dalšího levelu
                self.change_level()

    def render(self):
        self.screen.fill(background2)
        self.player.draw()
        self.npc.draw()

        if self.door_spawned:
            self.door.draw()



        # Aplikování masky pro zorné pole
        mask = pygame.Surface((screen_width, screen_height))
        mask.fill((0, 0, 0))
        # Použití pozic hráče z třídy Player
        pygame.draw.circle(mask, (255, 255, 255),(self.player.x + self.player.size // 2, self.player.y + self.player.size // 2), view_radius)
        mask.set_colorkey((255, 255, 255))
        self.screen.blit(mask, (0, 0))
        if self.door_spawned:
            pygame.draw.rect(self.screen, door_color, (self.door.x, self.door.y, door_width, door_height))
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= 5000:  # Zobraz text, pokud uplynulo méně než 5 sekund
            text_surf = self.font.render("I don't think I'm alone here...", True, (255, 255, 255))  # Bílý text
            text_rect = text_surf.get_rect(center=(screen_width // 2, 20))
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    def change_level(self):
        pygame.quit()
        subprocess.run(["python", "level3.py"])
        sys.exit()

    def quit(self):
        pygame.quit()
        sys.exit()

class MusicManager:
    def __init__(self):
        pygame.mixer.music.load(r'assets/music/main_menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.stop_sound = pygame.mixer.Sound(r'assets/music/music-stop.mp3')
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.pickup_sound = pygame.mixer.Sound(r'assets/sounds/pickup.mp3')
        self.music_playing = True

    def update(self):
        current_time = pygame.time.get_ticks()

class JumpscareManager:
    def __init__(self, screen):
        self.screen = screen
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.jumpscare_triggered = False
        self.music_stopped_time = None

    def update(self, music_playing, current_time):
        # Zaznamená čas, kdy hudba skončila
        if not music_playing and self.music_stopped_time is None:
            self.music_stopped_time = current_time
        elif music_playing:
            self.music_stopped_time = None  # Reset, pokud hudba znovu začne hrát

    def trigger_jumpscare(self):
        self.jumpscare_sound.play()
        self.screen.blit(self.jumpscare_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Jumpscare je zobrazen 3 sekundy
        pygame.quit()  # Ukončení Pygame

        # Vrátit se do hlavního menu
        subprocess.run(["python", "path_to_main_menu.py"])
        sys.exit()  # Ukončení skriptu

class Door:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = self.generate_random_door_position()

    def generate_random_door_position(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            return random.randint(0, screen_width - door_width), 0
        elif edge == "bottom":
            return random.randint(0, screen_width - door_width), screen_height - door_height
        elif edge == "left":
            return 0, random.randint(0, screen_height - door_height)
        else:  # edge == "right"
            return screen_width - door_width, random.randint(0, screen_height - door_height)

    def draw(self):
        if len(coins) == 0:  # Předpokládáme, že existuje reference na instanci hry
            pygame.draw.rect(self.screen, door_color, (self.x, self.y, door_width, door_height))

if __name__ == "__main__":
    level2()