import subprocess
import pygame
import sys
import random
from settings import *
from level1 import  level1
from main import Player

class level0:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.music_manager = MusicManager()
        self.jumpscare_manager = JumpscareManager(self.screen)
        self.player = Player(self.screen)
        self.door = Door(self.screen)
        self.coins = [self.generate_coin_position() for _ in range(num_coins)]  # Použijeme num_coins z settings.py
        self.total_coins = len(self.coins)  # Celkový počet mincí ve hře
        self.collected_coins = 0  # Počet sebraných mincí
        self.font = pygame.font.Font(font_path, font_size)
        self.door_spawned = False
        self.running = True
        self.main_loop()
        pygame.time.Clock().tick(60)

    def generate_coin_position(self):
        return (random.randint(0, screen_width - coin_size), random.randint(0, screen_height - coin_size))

    def check_coin_collision(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
        for coin in self.coins[:]:  # Iterujeme přes kopii seznamu mincí, abychom mohli bezpečně odstraňovat
            coin_rect = pygame.Rect(coin[0], coin[1], coin_size, coin_size)
            if player_rect.colliderect(coin_rect):
                self.coins.remove(coin)  # Odstranění mince po kolizi
                self.collected_coins += 1
                self.music_manager.pickup_sound.play()  # Přehrání zvuku sběru
            if not self.coins:  # Pokud jsou všechny mince sebrány
                self.door_spawned = True
                self.door.x, self.door.y = self.door.generate_random_door_position()

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

        # Zde předáváme klávesy do metody update()
        self.player.update()  # Předáváme aktuální stavy kláves
        self.music_manager.update()
        self.jumpscare_manager.update(music_playing, player_moving, current_time)
        self.check_coin_collision()

        if self.door_spawned:
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)
            door_rect = pygame.Rect(self.door.x, self.door.y, door_width, door_height)
            if player_rect.colliderect(door_rect):
                # Přechod do dalšího levelu
                self.change_level()

    def render(self):
        self.screen.blit(background0, (0, 0))

        # Vykreslení herních prvků před aplikací masky
        self.player.draw()
        if self.door_spawned:
            self.door.draw()
        for coin in self.coins:
            pygame.draw.rect(self.screen, (255, 215, 0), (coin[0], coin[1], coin_size, coin_size))

        # Aplikování masky pro zorné pole
        mask = pygame.Surface((screen_width, screen_height))
        mask.fill((0, 0, 0))

        # Výpočet středu hráče předpokládá, že self.player.size je výška a šířka je pevně nastavena na 60 pixelů
        player_center_x = self.player.x + 60 // 2  # Půlka šířky obrázku hráče
        player_center_y = self.player.y + 30 // 2  # Půlka výšky obrázku hráče, pokud player_size = 30

        # Vykreslení kruhu pro zorné pole s použitím upravených středových bodů
        pygame.draw.circle(mask, (255, 255, 255), (player_center_x, player_center_y), view_radius)
        mask.set_colorkey((255, 255, 255))
        self.screen.blit(mask, (0, 0))


        coins_text = f"{self.collected_coins} / {self.total_coins}"
        text_surf = self.font.render(coins_text, True, white)
        self.screen.blit(text_surf, (screen_width - text_surf.get_width() - 10, 10))  # Umístění v pravém horním rohu

        if len(self.coins) == 0:
            exit_message = "Great, now look for the exit"
            message_surf = self.font.render(exit_message, True, white)
            message_rect = message_surf.get_rect(center=(screen_width / 2, 20))
            self.screen.blit(message_surf, message_rect)
        pygame.display.flip()

    def change_level(self):
        pygame.quit()
        subprocess.run(["python", "level1.py"])
        sys.exit()

    def quit(self):
        pygame.quit()
        sys.exit()

class MusicManager:
    def __init__(self):
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
        current_time = pygame.time.get_ticks()
        if self.music_playing and current_time - self.last_stop_time > self.stop_interval:
            pygame.mixer.music.stop()
            self.stop_sound.play()
            self.music_playing = False
            self.last_stop_time = current_time
            self.stop_interval = random.randint(3000, 7000)  # Kratší čas pro restart hudby
        elif not self.music_playing and current_time - self.last_stop_time > self.stop_interval:
            pygame.mixer.music.play(-1)
            self.music_playing = True
            self.last_stop_time = current_time
            self.stop_interval = random.randint(10000, 20000)

class JumpscareManager:
    def __init__(self, screen):
        self.screen = screen
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.jumpscare_triggered = False
        self.music_stopped_time = None

    def update(self, music_playing, player_moving, current_time):
        # Zaznamená čas, kdy hudba skončila
        if not music_playing and self.music_stopped_time is None:
            self.music_stopped_time = current_time
        elif music_playing:
            self.music_stopped_time = None  # Reset, pokud hudba znovu začne hrát

        # Spustí jumpscare, pokud hudba skončila, hráč se pohybuje a uplynula více než 1 sekunda
        if self.music_stopped_time and player_moving and current_time - self.music_stopped_time > 1000 and not self.jumpscare_triggered:
            self.trigger_jumpscare()

    def trigger_jumpscare(self):
        self.screen.fill((0, 0, 0))
        self.jumpscare_sound.play()
        self.screen.blit(self.jumpscare_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Jumpscare je zobrazen 2 sekundy
        self.jumpscare_triggered = False
        self.music_stopped_time = None
        pygame.quit()
        subprocess.run(["python", "menu.py"])


class Door:
    def __init__(self, screen):
        self.door_spawn = pygame.mixer.Sound(r'assets/sounds/door_spawn.mp3')
        self.door_spawned = True
        self.screen = screen
        self.x, self.y = self.generate_random_door_position()
        # Načtení obrázku dveří
        self.image = pygame.image.load('assets/tiles/exit_door.png').convert_alpha()
        # Nastavení velikosti obrázku dveří (pokud je potřeba)
        self.image = pygame.transform.scale(self.image, (50, 100))

    def generate_random_door_position(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        self.door_spawn.play()
        if edge == "top":
            return random.randint(0, screen_width - 50), 0  # Aktualizováno pro šířku obrázku dveří
        elif edge == "bottom":
            return random.randint(0, screen_width - 50), screen_height - 100  # Aktualizováno pro výšku obrázku dveří
        elif edge == "left":
            return 0, random.randint(0, screen_height - 100)
        else:  # edge == "right"
            return screen_width - 50, random.randint(0, screen_height - 100)

    def draw(self):
        if self.door_spawned:  # Předpokládám, že door_spawned je aktualizováno správně
            # Vykreslení obrázku dveří místo obdélníku
            self.screen.blit(self.image, (self.x, self.y))



if __name__ == "__main__":
    level0()
