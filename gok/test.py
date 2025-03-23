import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CASEOH SIMULATOR")

# barvicky
BLACK = (32, 32, 32) # tmave zelena
WHITE = (0, 255, 0) #svetle zelena
GREEN = (0, 191, 255) # zuzova
DARK_BLUE = (64, 64, 64) #takova napul

# fontik
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, text_color, button_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

def main_menu():
    # tlacitka na main menu
    play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "EAT", WHITE, DARK_BLUE)
    languages_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "LANGUAGES", WHITE, DARK_BLUE)
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 125, 200, 50, "END THE SUFFERING", WHITE, DARK_BLUE)

    # takova ta vec diky ktery se muzete vratit a tak
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lmb
                    pos = pygame.mouse.get_pos()
                    if play_button.is_clicked(pos):
                        return "EAT"
                    elif languages_button.is_clicked(pos):
                        return "LANGUAGES"
                    elif quit_button.is_clicked(pos):
                        pygame.quit()
                        sys.exit()

        # cisticka
        SCREEN.fill(BLACK)

        # obzivne textik
        text = font.render("CASEOH SIMULATOR", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(text, text_rect)

        # obzivnou tlacitka
        play_button.draw(SCREEN)
        languages_button.draw(SCREEN)
        quit_button.draw(SCREEN)

        pygame.display.flip()

def language_selection():
    # byla to puvodne anglictina ale cestina better
    english_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "burgir language", WHITE, DARK_BLUE)

    # looptyloop pro vyber jazyku
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lmb
                    pos = pygame.mouse.get_pos()
                    if english_button.is_clicked(pos):
                        return "NEVER BACK DOWN NEVER WHAT"  # tohle te posle zpatky proste

        # cisticka 2.0
        SCREEN.fill(BLACK)

        # obzivne vic textiku
        text = font.render("YOU HAVE NO CHOICE", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(text, text_rect)

        # obzivne cool tlacitko ktery vlastne neni pro anglictinu ale who cares na kod se stejne nikdo nediva ^^
        english_button.draw(SCREEN)

        pygame.display.flip()

def game_loop():
    # snejcik
    snake_block = 20
    snake_speed = 20

    # da snejcika na prostredek
    snake_x = SCREEN_WIDTH // 2
    snake_y = SCREEN_HEIGHT // 2
    snake_x_change = 0
    snake_y_change = 0

    # udela snejcikovi telicko
    snake_list = []
    snake_length = 1

    # jidlo pro snejka
    food_x = random.randrange(0, SCREEN_WIDTH - snake_block, snake_block)
    food_y = random.randrange(0, SCREEN_HEIGHT - snake_block, snake_block)

    # skore (tloustkometr)
    score = 350

    # tohle jsem totalne vymyslel sam :)
    snake_move_timer = pygame.time.get_ticks()

    # loopdyloop na kterem zavisi cela hra a pokud se pozmeni jeden detail tak jsem v pici protoze uz to nikdy fungovat nebude
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_x_change == 0:
                    snake_x_change = -snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT and snake_x_change == 0:
                    snake_x_change = snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_UP and snake_y_change == 0:
                    snake_y_change = -snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN and snake_y_change == 0:
                    snake_y_change = snake_block
                    snake_x_change = 0

        # snejk move
        if pygame.time.get_ticks() - snake_move_timer > 1000 // snake_speed:
            snake_x += snake_x_change
            snake_y += snake_y_change
            snake_move_timer = pygame.time.get_ticks()

            # yamyam
            if snake_x == food_x and snake_y == food_y:
                food_x = random.randrange(0, SCREEN_WIDTH - snake_block, snake_block)
                food_y = random.randrange(0, SCREEN_HEIGHT - snake_block, snake_block)
                snake_length += 1
                score += 1

            # update na tlustsiho
            snake_head = []
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            # aby nemohl bourat sam do sebe
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    return score

        # aby nemohl zdrhnout z PyGamu a znicit internet
        if (snake_x < 0 or snake_x >= SCREEN_WIDTH or
            snake_y < 0 or snake_y >= SCREEN_HEIGHT):
            return score

        # cisticka 3.0
        SCREEN.fill(BLACK)

        # zrozeni jidla
        pygame.draw.rect(SCREEN, GREEN, [food_x, food_y, snake_block, snake_block])

        # zrozeni snejka
        for segment in snake_list:
            pygame.draw.rect(SCREEN, WHITE, [segment[0], segment[1], snake_block, snake_block])

        # tloustkometr - zrozeni
        score_text = font.render(f"accurate weight: {score}lb", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()

def game_over(final_score):
    # setupnuti tlacitka na vypnuti programu
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 125, 200, 50, "END THE SUFFERING", WHITE, DARK_BLUE)

    # gejm ovr
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lmb
                    pos = pygame.mouse.get_pos()
                    if quit_button.is_clicked(pos):
                        pygame.quit()
                        sys.exit()

        # 350ta cisticka
        SCREEN.fill(BLACK)

        # vic textu
        text = font.render("died of hunger :p", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        SCREEN.blit(text, text_rect)

        # finalni skore :)
        score_text = font.render(f"FINAL WEIGHT: {final_score}LB", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        SCREEN.blit(score_text, score_rect)

        # amazing unique technology so you dont have to restart the whole fucking program
        restart_text = font.render("PRESS SPACE AND START EATING AGAIN", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        SCREEN.blit(restart_text, restart_rect)
        
        # self kill button
        quit_button.draw(SCREEN)

        pygame.display.flip()

# mejn menu luup
while True:
    selection = main_menu()
    if selection == "EAT":
        # gejm luup - pokracovani
        while True:
            final_score = game_loop()
            game_over(final_score)
    elif selection == "LANGUAGES":
        selection = language_selection()
        if selection == "NEVER BACK DOWN NEVER WHAT":  # abys sel zpatky po stisknuti tlacitka
            continue

# smrt programu
pygame.quit()
