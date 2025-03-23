import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Soccer Ball")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# Set up initial positions and velocities
ball_radius = 25
ball_x, ball_y = screen_width // 2, screen_height // 2
ball_dx, ball_dy = 5, 5
angle = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Draw the brown line
    pygame.draw.line(screen, BROWN, (0, screen_height // 2), (screen_width, screen_height // 2), 5)

    # Draw and rotate the triangle
    triangle_points = [
        (ball_x + ball_radius * math.cos(math.radians(angle)), ball_y + ball_radius * math.sin(math.radians(angle))),
        (ball_x + ball_radius * math.cos(math.radians(angle + 120)), ball_y + ball_radius * math.sin(math.radians(angle + 120))),
        (ball_x + ball_radius * math.cos(math.radians(angle + 240)), ball_y + ball_radius * math.sin(math.radians(angle + 240)))
    ]
    pygame.draw.polygon(screen, BLACK, triangle_points)

    # Update angle
    angle -= 5 if ball_dx > 0 else -5

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_dx = -ball_dx

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()