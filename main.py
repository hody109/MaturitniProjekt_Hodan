from menu import MainMenu
from settings import *

class Player:
    """
    A class representing the player character in the game.

    :param screen: Pygame screen object where the player will be drawn.
    :type screen: pygame.Surface
    """
    def __init__(self, screen):
        self.screen = screen
        self.x = 10
        self.y = 10
        self.speed = player_speed
        self.size = player_size
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        self.player_img = pygame.image.load(r'assets/tiles/player.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (60, 30))
        self.player_left = pygame.transform.rotate(self.player_img, -90)
        self.player_right = pygame.transform.rotate(self.player_img, 90)
        self.player_up =pygame.transform.rotate(self.player_img, 180)
        self.player_down = self.player_img
        self.interact = False
        self.footstep_sound = pygame.mixer.Sound(r'assets/sounds/footstep.mp3')
        self.footstep_sound.set_volume(0.5)
        self.is_playing_footsteps = False

    def handle_event(self, event):
        """
        Handles key press and release events to control player movement and interactions.

        :param event: The event object from the pygame event queue.
        :type event: pygame.event.Event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
                self.player_img = self.player_left
            elif event.key == pygame.K_RIGHT:
                self.move_right = True
                self.player_img = self.player_right
            elif event.key == pygame.K_UP:
                self.move_up = True
                self.player_img = self.player_up
            elif event.key == pygame.K_DOWN:
                self.move_down = True
                self.player_img = self.player_down
            elif event.key == pygame.K_SPACE:
                self.interact = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False
            elif event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False
            elif event.key == pygame.K_SPACE:
                self.interact = False

    def is_moving(self):
        """
        Check if the player is currently moving.

        :return: Returns True if the player is moving in any direction, False otherwise.
        :rtype: bool
        """
        if self.move_left or self.move_right or self.move_up or self.move_down:
            if not self.is_playing_footsteps:
                self.footstep_sound.play(loops=-1)  # Loop the sound
                self.is_playing_footsteps = True
        else:
            if self.is_playing_footsteps:
                self.footstep_sound.stop()
                self.is_playing_footsteps = False



    def update(self):
        """
        Update the player's position based on movement flags.
        """
        if self.move_left:
            self.x -= self.speed
            self.moving = True
        if self.move_right:
            self.x += self.speed
            self.moving = True
        if self.move_up:
            self.y -= self.speed
            self.moving = True
        if self.move_down:
            self.y += self.speed
            self.moving = True

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.rect.x = max(0, min(self.rect.x, screen_width - self.size))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.size))



    def draw(self):
        """
        Draw the player on the screen at the updated position.
        """
        image_center_x = self.rect.x - self.player_img.get_width() // 2
        image_center_y = self.rect.y - self.player_img.get_height() // 2

        self.screen.blit(self.player_img, (image_center_x, image_center_y))


class NPC:
    """
    A class representing a non-player character in the game that interacts with the player.

    :param screen: Pygame screen object where the NPC will be drawn.
    :param player: A reference to the player object.
    :type screen: pygame.Surface
    :type player: Player
        """
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = monster_speed
        self.chase_speed = 2.5
        self.size = monster_size
        self.vision_radius = 150
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.distance_moved = 0
        self.move_distance_limit = random.randint(50, 150)
        self.chase_sound = pygame.mixer.Sound(r'assets/sounds/skin_stealer.mp3')
        self.jumpscare_sound = pygame.mixer.Sound(r'assets/sounds/jumpscare.mp3')
        self.jumpscare_image = pygame.image.load(r'assets/images/jumpscare.png').convert_alpha()
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (screen_width, screen_height))
        self.is_chasing = False
        self.monster_img = pygame.image.load(r'assets/tiles/monster.png').convert_alpha()
        self.monster_img = pygame.transform.scale(self.monster_img, (60, 30))
        self.monster_left = pygame.transform.rotate(self.monster_img, -90)
        self.monster_right = pygame.transform.rotate(self.monster_img, 90)
        self.monster_up = pygame.transform.rotate(self.monster_img, 180)
        self.monster_down = self.monster_img
        self.current_img = self.monster_down

    def expand_vision(self, new_radius):
        """
        Expand the NPC's vision radius.

        :param new_radius: The new radius of vision for the NPC.
        :type new_radius: int
        """
        self.vision_radius = new_radius

    def move_randomly(self):
        """
        Move the NPC in a random direction until a set limit is reached, then choose a new direction.
        """
        if self.distance_moved >= self.move_distance_limit:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.distance_moved = 0
            self.move_distance_limit = random.randint(50, 150)

        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed

        self.distance_moved += self.speed
        self.x = max(0, min(self.x, screen_width - self.size))
        self.y = max(0, min(self.y, screen_height - self.size))

    def chase_player(self):
        """
        Chase the player if they enter the NPC's vision radius.
        """
        self.chase_sound.play()
        self.chase_sound.set_volume(0.5)
        self.is_chasing = True
        if self.x < self.player.x:
            self.x += self.chase_speed
        if self.x > self.player.x:
            self.x -= self.chase_speed
        if self.y < self.player.y:
            self.y += self.chase_speed
        if self.y > self.player.y:
            self.y -= self.chase_speed

    def update(self):
        """
        Update the NPC's state, including position, and check for interactions with the player.
        """
        self.rect.x = self.x
        self.rect.y = self.y
        if pygame.math.Vector2(self.x - self.player.x, self.y - self.player.y).length() < self.vision_radius:
            self.chase_player()
        else:
            self.move_randomly()

        if self.direction == 'left':
            self.current_img = self.monster_right
        elif self.direction == 'right':
            self.current_img = self.monster_left
        elif self.direction == 'up':
            self.current_img = self.monster_down
        elif self.direction == 'down':
            self.current_img = self.monster_up

        if self.rect.colliderect(self.player.rect):
            self.screen.fill((0, 0, 0))
            self.chase_sound.stop()
            self.jumpscare_sound.play()
            self.screen.blit(self.jumpscare_image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            subprocess.run(["python", "main.py"])
            sys.exit()

    def draw(self):
        """
        Draw the NPC on the screen at the updated position.
        """
        image_center_x = self.x - self.current_img.get_width() // 2
        image_center_y = self.y - self.current_img.get_height() // 2

        self.screen.blit(self.current_img, (image_center_x, image_center_y))

if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu()