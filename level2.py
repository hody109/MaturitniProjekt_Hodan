import subprocess
import pygame
import sys
import random
from settings import *
from main import Player
from main import NPC

class Computer:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(r'assets/tiles/computer.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 150))  # Změna velikosti na šířku 100 a výšku 150
        self.rect = self.image.get_rect(center=(x, y))  # Centrování na zadané x, y
        self.font = pygame.font.Font(None, 48)  # Větší font pro otázku a odpověď
        self.question = "What am I? :"
        self.active = False
        self.answer = ""
        self.show_input = False
        self.computer_sound = pygame.mixer.Sound(r'assets/sounds/computer.mp3')

    def draw(self):
        self.screen.blit(self.image, self.rect)



    def check_answer(self, answer):
        if answer.lower() == "balloon":
            pygame.quit()
            subprocess.run(["python", "level3_end.py"])
            sys.exit()


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
        self.table = InteractiveObject(self.screen, screen_width // 2, screen_height // 2, 150, 100)
        self.computer = Computer(self.screen, screen_width - 50, screen_height // 2)
        self.countdown_started = False
        self.countdown_time = 35  # Počáteční doba odpočtu
        self.countdown_start_ticks = None
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.computer.rect.colliderect(self.player.rect):
                        self.computer.active = True
                        self.computer.show_input = True
                        self.computer.computer_sound.play()
                elif self.computer.show_input:
                    if event.key == pygame.K_RETURN:
                        self.computer.check_answer(self.computer.answer)
                        self.computer.answer = ""  # Reset po zadání odpovědi
                        self.computer.show_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.computer.answer = self.computer.answer[:-1]
                    else:
                        self.computer.answer += event.unicode

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
        if self.table.rect.colliderect(self.player.rect) and self.player.interact:
            if not self.countdown_started:
                self.countdown_started = True
                self.countdown_start_ticks = pygame.time.get_ticks()
            self.table.play_sound()

        if self.countdown_started:
            elapsed_time = (pygame.time.get_ticks() - self.countdown_start_ticks) // 1000
            self.countdown_time = max(0, 35 - elapsed_time)  # Aby čas nepoklesl pod nulu

        if self.countdown_time == 0:
            self.npc.expand_vision(2000)  # Rozšíření vision radius na 2000

    def render(self):
        self.screen.fill(background2)
        self.player.draw()
        self.npc.draw()
        self.table.draw()
        self.computer.draw()

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
        if self.countdown_started:
            countdown_text = self.font.render(f'{self.countdown_time}s', True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(topright=(screen_width - 20, 20))
            self.screen.blit(countdown_text, countdown_rect)
        if self.computer.active and self.computer.show_input:
            # Centrování textu na obrazovce
            question_surface = self.font.render(self.computer.question, True, (255, 255, 255))
            question_rect = question_surface.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
            self.screen.blit(question_surface, question_rect)
            answer_surface = self.font.render(self.computer.answer, True, (255, 255, 255))
            answer_rect = answer_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(answer_surface, answer_rect)
        pygame.display.flip()

    def change_level(self):
        pygame.quit()
        subprocess.run(["python", "level3_end.py"])
        sys.exit()

    def quit(self):
        pygame.quit()
        sys.exit()




class InteractiveObject:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.image = pygame.image.load(r'assets/tiles/table.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 100))  # Změna velikosti na šířku 150 a výšku 100
        self.rect = self.image.get_rect(center=(x, y))
        self.interact_sound = pygame.mixer.Sound(r'assets/sounds/hadanka.mp3')

    def draw(self):
        self.screen.blit(self.image, self.rect)
    def play_sound(self):
        self.interact_sound.play()
        self.show_question = True
        self.question_time = pygame.time.get_ticks()

    def update(self):
        if self.show_question:
            current_time = pygame.time.get_ticks()
            if current_time - self.question_time > 35000:
                self.show_question = False


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