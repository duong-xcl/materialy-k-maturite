import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
FPS = 60

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Get the absolute path of the script directory
BASE_DIR = os.path.dirname(__file__)

# Load images with absolute paths
heart = pygame.image.load(os.path.join(BASE_DIR, "heart.png"))
heartbroken = pygame.image.load(os.path.join(BASE_DIR, "heartbroken.png"))

# Load sound
death_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "death.mp3"))

# Resize images (if needed)
HEART_SIZE = 50
heart = pygame.transform.scale(heart, (HEART_SIZE, HEART_SIZE))
heartbroken = pygame.transform.scale(heartbroken, (HEART_SIZE, HEART_SIZE))

# Fragment class
class Fragment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.choice([-3, 3])
        self.vel_y = random.randint(-5, -2)
        self.rotation = random.uniform(-5, 5)  # Random rotation speed
        self.angle = 0
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (210, 0, 0), [(0, 0), (15, 7), (7, 15)])
        self.original_image = self.image.copy()

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.3  # Gravity effect
        self.angle += self.rotation  # Apply rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, surface):
        rotated_rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rotated_rect.topleft)

# Main function
def main():
    running = True
    stage = 0  # 0 = normal, 1 = broken, 2 = exploding
    timer = pygame.time.get_ticks()
    fragments = []
    sound_played = False
    
    heart_x, heart_y = WIDTH // 2 - HEART_SIZE // 2, HEIGHT // 2 - HEART_SIZE // 2
    
    while running:
        display.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        current_time = pygame.time.get_ticks()
        
        if stage == 0:
            display.blit(heart, (heart_x, heart_y))
            if current_time - timer > 1000:  # Show heart for 1 second
                stage = 1
                timer = pygame.time.get_ticks()
        elif stage == 1:
            display.blit(heartbroken, (heart_x, heart_y))
            if not sound_played:
                death_sound.play()
                sound_played = True
            if current_time - timer > 1400:  # Show heartbroken for 1.4 seconds
                stage = 2
                timer = pygame.time.get_ticks()
                for _ in range(3):
                    fragments.append(Fragment(heart_x + HEART_SIZE // 2, heart_y + HEART_SIZE // 2))
        elif stage == 2:
            for fragment in fragments:
                fragment.update()
                fragment.draw(display)
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
