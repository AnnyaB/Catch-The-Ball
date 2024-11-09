import pygame
import random
import time

# Initializing Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Catch Ball Game")

# Defining colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Defining player settings
player_width = 50
player_height = 10
player_speed = 5

# Loading sound effects
catch_sound = pygame.mixer.Sound("catch_sound.wav")  # Add path to your catch sound file
wall_hit_sound = pygame.mixer.Sound("wall_hit_sound.wav")  # Add path to your wall hit sound file

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += player_speed
        # Prevent players from going out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.x_velocity = random.choice([3, -3])
        self.y_velocity = random.choice([3, -3])

    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.x_velocity *= -1
            wall_hit_sound.play()  # Play wall hit sound

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.y_velocity *= -1
            wall_hit_sound.play()  # Play wall hit sound

# Game setup
player1 = Player(RED, WIDTH // 4, HEIGHT - 30)
player2 = Player(BLUE, 3 * WIDTH // 4, HEIGHT - 30)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2, ball)

# Score variables
score_player1 = 0
score_player2 = 0

# Font for score display
font = pygame.font.SysFont(None, 36)

# Timer for game duration
game_start_time = time.time()  # Start time for the game
game_duration = 120  # Game duration in seconds (2 minutes)

# Main game loop
running = True
clock = pygame.time.Clock()

# Player selection
player_choice = None

while running:
    screen.fill(WHITE)

    # Player selection screen
    if player_choice is None:
        text1 = font.render("Press 1 for Player 1 (Red)", True, (0, 0, 0))
        text2 = font.render("Press 2 for Player 2 (Blue)", True, (0, 0, 0))
        screen.blit(text1, (WIDTH // 4, HEIGHT // 3))
        screen.blit(text2, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

        # Wait for player choice
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_choice = 'player1'
                if event.key == pygame.K_2:
                    player_choice = 'player2'

    # Game logic after player selection
    if player_choice is not None:
        keys = pygame.key.get_pressed()

        # Updating players
        if player_choice == 'player1':
            player1.update(keys)
        else:
            player2.update(keys)

        # Updating ball
        ball.update()

        # Checking for collision (catching the ball)
        if pygame.sprite.collide_rect(player1, ball):
            ball.x_velocity *= -1
            ball.y_velocity *= -1
            score_player1 += 1  # Increment score for Player 1
            catch_sound.play()  # Play catch sound

        if pygame.sprite.collide_rect(player2, ball):
            ball.x_velocity *= -1
            ball.y_velocity *= -1
            score_player2 += 1  # Increment score for Player 2
            catch_sound.play()  # Play catch sound

        # Gradually increasing ball speed after every 5 points scored
        if score_player1 % 5 == 0 or score_player2 % 5 == 0:
            ball.x_velocity *= 1.1  # Increase speed by 10%
            ball.y_velocity *= 1.1

        # Displaying score
        score_text = font.render(f"Player 1: {score_player1}  Player 2: {score_player2}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 3, 20))

        # Drawing everything
        all_sprites.draw(screen)

        # Checking if 2 minutes have passed
        if time.time() - game_start_time > game_duration:
            running = False  # End game after 2 minutes
            text_end = font.render("Game Over! Do you want to play again? (Y/N)", True, (0, 0, 0))
            screen.blit(text_end, (WIDTH // 4, HEIGHT // 3))
            pygame.display.flip()

            # Waiting for user input
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_for_input = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            # Restart the game
                            score_player1 = 0
                            score_player2 = 0
                            game_start_time = time.time()  # Reset timer
                            player_choice = None  # Restart player selection
                            waiting_for_input = False
                        elif event.key == pygame.K_n:
                            # Exit the game
                            running = False
                            waiting_for_input = False

        pygame.display.flip()

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()
