import pygame
import sys
import subprocess
import os

class MainMenu:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen
        pygame.init()
        self.screen_width, self.screen_height = 800, 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Escape the Mazerooms - Main Menu")
        self.background_image = pygame.image.load(r'assets/images/background_menu.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.font_path = r'assets/fonts/ScreamAgain.ttf'
        self.font_size = 15
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.title_font_size = 40
        self.title_font = pygame.font.Font(self.font_path, self.title_font_size)
        self.menu_items = ['Play', 'Tutorial', 'Magazine','Quit']
        self.tutorial_image = pygame.image.load(r'assets/images/tutorial.jpg').convert()
        self.magazine_image = pygame.image.load(r'assets/images/Magazine.jpg').convert()
        self.tutorial_image = pygame.transform.scale(self.tutorial_image, (self.screen_width, self.screen_height))
        self.magazine_image = pygame.transform.scale(self.magazine_image, (self.screen_width, self.screen_height))
        self.menu_colors = {'normal': (255, 255, 255), 'hover': (255, 215, 0), 'click': (255, 0, 0), 'title': (0, 0, 0)}
        self.menu_rects = []
        self.return_button_color = (255, 255, 255)
        self.start_background_music()
        self.state = 'menu'

    def return_to_menu(self):
        self.state = 'menu'
        self.main_menu()
    def start_background_music(self):
        pygame.mixer.music.load(r'assets/music/main_menu.mp3')
        pygame.mixer.music.play(-1)

    def draw_menu(self):
        if self.state != 'menu':
            return
        self.screen.blit(self.background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        title_text = self.title_font.render("Escape the Mazerooms", True, self.menu_colors['title'])
        title_position = title_text.get_rect(center=(self.screen_width / 2, 100))
        self.screen.blit(title_text, title_position)

        self.menu_rects.clear()
        for index, item in enumerate(self.menu_items):
            hover = self.menu_rects[index].collidepoint(mouse_pos) if index < len(self.menu_rects) else False
            color = self.menu_colors['hover'] if hover else self.menu_colors['normal']
            text = self.font.render(item, True, color)
            position = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + index * 50 + 50))
            self.menu_rects.append(position)
            self.screen.blit(text, position)
        pygame.display.flip()


    def draw_return_button(self):
        button_text = "Return"
        text_surf = self.font.render(button_text, True, self.return_button_color)
        text_rect = text_surf.get_rect(center=(self.screen_width / 2, self.screen_height - 50))
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10))
        self.screen.blit(text_surf, text_rect)
        return text_rect

    def show_tutorial(self):
        self.state = 'tutorial'
        running = True
        return_button_rect = self.draw_return_button()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if return_button_rect and return_button_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.time.wait(300)
                        self.return_button_color = (255, 0, 0)
                        self.return_to_menu()
                        return
            if self.state == 'menu':
                return
            self.screen.blit(self.tutorial_image, (0, 0))
            self.menu_rects.clear()
            return_button_rect = self.draw_return_button()
            pygame.display.flip()
            self.return_button_color = (255, 255, 255)

    def show_magazine(self):
        self.state = 'magazine'
        running = True
        return_button_rect = self.draw_return_button()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if return_button_rect and return_button_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.time.wait(300)
                        self.return_button_color = (255, 0, 0)
                        self.return_to_menu()
                        return
            if self.state == 'menu':
                return

            self.screen.blit(self.magazine_image, (0, 0))
            self.menu_rects.clear()
            return_button_rect = self.draw_return_button()
            pygame.display.flip()
            self.return_button_color = (255, 255, 255)

    def play_click_animation_and_proceed(self, index):
        text = self.font.render(self.menu_items[index], True, self.menu_colors['click'])
        self.screen.blit(text, self.menu_rects[index])
        pygame.display.flip()
        pygame.time.wait(300)

        if self.menu_items[index] == 'Tutorial':
            self.show_tutorial()
            self.state = 'menu'
        elif self.menu_items[index] == 'Magazine':
            self.show_magazine()
            self.state = 'menu'
        elif self.menu_items[index] == 'Play':
            pygame.mixer.music.stop()
            self.start_background_music()
            pygame.quit()
            subprocess.run(["python", "intro.py"])
            sys.exit()
        elif self.menu_items[index] == 'Quit':
            pygame.quit()
            sys.exit()

    def main_menu(self):
        self.draw_menu()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for index, rect in enumerate(self.menu_rects):
                        if rect.collidepoint(pos):
                            self.play_click_animation_and_proceed(index)

            pygame.display.update()

if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu()
