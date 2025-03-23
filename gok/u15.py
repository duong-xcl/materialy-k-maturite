import pygame
pygame.init()
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)
square_color = (255, 0, 0)
square_pos = (150, 150)
square_size = 100
pygame.draw.rect(screen, square_color, (square_pos[0], square_pos[1], square_size, square_size))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
