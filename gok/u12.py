import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Box")

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 100)

# Fonts
font = pygame.font.Font(None, 32)

# Textbox properties
textbox_rect = pygame.Rect(50, 50, 300, 50)
textbox_color = GRAY
text = ''

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if textbox_rect.collidepoint(event.pos):
                textbox_color = BLUE
            else:
                textbox_color = GRAY
        elif event.type == pygame.KEYDOWN:
            if textbox_color == BLUE:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Entered text:", text)
                    text = ''
                else:
                    text += event.unicode

    # Clear the screen
    screen.fill(BLACK)

    # Draw the textbox
    pygame.draw.rect(screen, textbox_color, textbox_rect)
    pygame.draw.rect(screen, (0, 0, 0), textbox_rect, 2)

    # Render the text
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (textbox_rect.x + 5, textbox_rect.y + 5))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()