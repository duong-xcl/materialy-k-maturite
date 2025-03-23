import pygame
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RETRO_BLUE = (0, 255, 255)
RETRO_GREEN = (0, 255, 0)
PLAYER_SIZE = 50
GROUND_HEIGHT = 20
GRAVITY = 1
JUMP_STRENGTH = 20
HOLE_FREQUENCY = 100  # Higher values reduce hole frequency

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump Across Gaps")

# Clock to control frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RETRO_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_SIZE
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check if the player hits the ground
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

# Hole class
class Hole(pygame.sprite.Sprite):
    def __init__(self, x, width):
        super().__init__()
        self.image = pygame.Surface((width, GROUND_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Initialize player
player = Player()

# Create sprite groups
all_sprites = pygame.sprite.Group()
holes = pygame.sprite.Group()
all_sprites.add(player)

# Function to generate holes
def generate_holes(last_hole_x):
    x = last_hole_x
    while x < SCREEN_WIDTH + 1000:
        if random.randint(1, HOLE_FREQUENCY) < 10:  # Adjust this value to change the frequency of holes
            width = random.randint(50, 150)
            hole = Hole(x, width)
            holes.add(hole)
            all_sprites.add(hole)
            x += width
        else:
            x += 200  # Distance between holes
    return x

# Generate initial holes
last_hole_x = generate_holes(0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Generate new holes if needed
    if len(holes) < 5:
        last_hole_x = generate_holes(last_hole_x)

    # Collision detection
    collisions = pygame.sprite.spritecollide(player, holes, False)
    if collisions:
        running = False  # End game if player falls into a hole

    # Clear screen
    screen.fill(RETRO_GREEN)

    # Draw ground with holes
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    holes.draw(screen)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()