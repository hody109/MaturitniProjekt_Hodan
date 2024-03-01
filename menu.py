import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape the Mazerooms - Main Menu")

# Load background image
background_image = pygame.image.load(r'assets/images/background_menu.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


# Function to start or restart background music
def start_background_music():
    pygame.mixer.music.load(r'assets/music/main_menu.mp3')
    pygame.mixer.music.play(-1)  # Play the music in a loop


# Start background music initially
start_background_music()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)  # Color for the click animation
gold = (255, 215, 0)  # Color for the title

# Font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)  # Larger font for the title

# Menu options and their rectangles for click detection
menu_items = ['Hrát', 'Ukončit']
menu_rects = []


def draw_menu():
    screen.blit(background_image, (0, 0))  # Use the background image

    # Draw the title
    title_text = title_font.render("Escape the Mazerooms", True, black)
    title_position = title_text.get_rect(center=(screen_width / 2, 100))
    screen.blit(title_text, title_position)

    menu_rects.clear()  # Clear the previous rectangles
    for index, item in enumerate(menu_items):
        text = font.render(item, True, white)
        position = text.get_rect(center=(screen_width / 2, screen_height / 2 + index * 50 + 50))
        menu_rects.append(position)  # Store the rectangle for click detection
        screen.blit(text, position)
    pygame.display.flip()


def play_click_animation_and_proceed(index):
    # Simple "animation" by changing color
    text = font.render(menu_items[index], True, red)
    screen.blit(text, menu_rects[index])
    pygame.display.flip()
    pygame.time.wait(300)  # Wait a bit to simulate animation

    # Proceed based on the index
    if index == 0:  # Hrát
        pygame.mixer.music.stop()  # Stop the music before launching the game
        subprocess.run(["python", "main.py"])
        start_background_music()  # Restart the music when returning to the menu
    elif index == 1:  # Ukončit
        pygame.quit()
        sys.exit()


def main_menu():
    draw_menu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                for index, rect in enumerate(menu_rects):
                    if rect.collidepoint(pos):
                        play_click_animation_and_proceed(index)

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
