import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake attributes
BLOCK_SIZE = 20
SNAKE_SPEED = 10

# Fonts
FONT = pygame.font.SysFont(None, 30)

# Functions
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(SCREEN, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_food(food_pos):
    pygame.draw.rect(SCREEN, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])

def message(text, color):
    text_surface = FONT.render(text, True, color)
    SCREEN.blit(text_surface, [WIDTH/2 - text_surface.get_width()/2, HEIGHT/2])

def start_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        SCREEN.fill(BLACK)
        message("Press SPACE to Play", WHITE)
        pygame.display.update()

def game_loop():
    # Snake initial position
    snake = [[WIDTH/2, HEIGHT/2]]
    snake_length = 1

    # Snake movement
    dx = 0
    dy = 0

    # Food initial position
    food_pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = BLOCK_SIZE

        # Move the snake
        snake[0][0] += dx
        snake[0][1] += dy

        # Check for collision with the food
        if snake[0][0] == food_pos[0] and snake[0][1] == food_pos[1]:
            food_pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
            snake_length += 1

        # Check for collision with the screen boundaries
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            game_over = True

        # Check for collision with itself
        for block in snake[1:]:
            if snake[0][0] == block[0] and snake[0][1] == block[1]:
                game_over = True

        # Move the rest of the snake
        for i in range(len(snake)-1, 0, -1):
            snake[i] = [snake[i-1][0], snake[i-1][1]]

        # Grow the snake when it eats food
        while len(snake) < snake_length:
            snake.append([snake[-1][0], snake[-1][1]])

        # Draw everything
        SCREEN.fill(BLACK)
        draw_snake(snake)
        draw_food(food_pos)

        # Refresh the screen
        pygame.display.update()

        # FPS
        clock.tick(SNAKE_SPEED)

    # Display Game Over message
    message("Game Over!", WHITE)
    pygame.display.update()
    pygame.time.wait(2000)

    pygame.quit()
    quit()

start_screen()
game_loop()