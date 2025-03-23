import pygame
import random

# Initialize PyGame
pygame.init()

# Define Colors
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
INITIAL_ENEMY_SPEED = 5
ENEMY_INCREMENT = 0.5
NEAR_MISS_DISTANCE = 25

# Create the Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Define the Player Block
player_pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_SIZE - 10]

# Define the Enemy Block
enemy_list = []

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, YELLOW, (enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE))

def update_enemy_positions(enemy_list, enemy_speed):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x + ENEMY_SIZE)):
        if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y + ENEMY_SIZE)):
            return True
    return False

def detect_near_miss(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if abs(p_x - e_x) < PLAYER_SIZE and abs(p_y - e_y) < PLAYER_SIZE + NEAR_MISS_DISTANCE and not detect_collision(player_pos, enemy_pos):
        return True
    return False

def main_menu():
    screen.fill(BLACK)
    font = pygame.font.SysFont("monospace", 75)
    label = font.render("zacni", 1, WHITE)
    play_button = label.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(label, play_button)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    waiting = False

# Game Loop
game_over = False
clock = pygame.time.Clock()
score = 0
enemy_speed = INITIAL_ENEMY_SPEED
start_ticks = pygame.time.get_ticks()  # for timing
score_ticks = pygame.time.get_ticks()  # for score timing
menu = True
near_miss_display_time = 0
near_miss_message = False

while not game_over:
    if menu:
        main_menu()
        menu = False
        start_ticks = pygame.time.get_ticks()
        score_ticks = pygame.time.get_ticks()
        score = 0
        enemy_speed = INITIAL_ENEMY_SPEED
        enemy_list = []
        player_pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_SIZE - 10]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - PLAYER_SIZE:
        player_pos[0] += 10

    screen.fill(BLACK)

    drop_enemies(enemy_list)
    update_enemy_positions(enemy_list, enemy_speed)

    # Increase difficulty every 10 seconds
    if (pygame.time.get_ticks() - start_ticks) > 10000:
        enemy_speed += ENEMY_INCREMENT
        start_ticks = pygame.time.get_ticks()

    # Increase score every 3 seconds
    if (pygame.time.get_ticks() - score_ticks) > 3000:
        score += 1
        score_ticks = pygame.time.get_ticks()

    if collision_check(enemy_list, player_pos):
        game_over = True
        break

    for enemy_pos in enemy_list:
        if detect_near_miss(player_pos, enemy_pos):
            score += 2
            near_miss_display_time = pygame.time.get_ticks()
            near_miss_message = True

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    font = pygame.font.SysFont("monospace", 35)
    text = "Score: " + str(score)
    label = font.render(text, 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40))

    # Display "NEAR MISS +2" message for a short time
    if near_miss_message:
        near_miss_font = pygame.font.SysFont("monospace", 50)
        near_miss_label = near_miss_font.render("NEAR MISS +2", 1, YELLOW)
        screen.blit(near_miss_label, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2))
        if pygame.time.get_ticks() - near_miss_display_time > 1000:  # Display for 1 second
            near_miss_message = False

    pygame.display.update()

    clock.tick(30)

print("Game Over! Your score was: ", score)
pygame.quit()
