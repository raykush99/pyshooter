import pygame

pygame.init()
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centered Text")

font = pygame.font.Font(None, 48)  # Default font, size 48
color = (2, 255, 255)  # White color
# Get the rect of the text surface and center it
text_rect = font.render("Hello, Kush!", True, color).get_rect(center=(WIDTH // 2, HEIGHT // 2))

running = True
while running:
    screen.fill((30, 30, 30))  # Dark background
    screen.blit(font.render("Hello, Kush!", True, color), text_rect)  # Draw centered text

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()