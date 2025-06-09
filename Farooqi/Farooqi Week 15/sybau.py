import pygame
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gurt gurt sybau")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (200, 200, 200)
BG = (180, 220, 255)
YELLOW = (255, 220, 100)

def draw_goose(surface, x, y):
    # Body
    pygame.draw.ellipse(surface, WHITE, (x, y+40, 120, 60))  # body
    # Wing
    pygame.draw.ellipse(surface, GREY, (x+40, y+55, 50, 30))
    # Neck
    pygame.draw.rect(surface, WHITE, (x+90, y+10, 18, 50), border_radius=9)
    # Head
    pygame.draw.ellipse(surface, WHITE, (x+95, y, 30, 30))
    # Beak
    pygame.draw.polygon(surface, ORANGE, [(x+120, y+15), (x+140, y+20), (x+120, y+25)])
    # Eye
    pygame.draw.circle(surface, BLACK, (x+115, y+15), 3)

def draw_text_bubble(surface, x, y, text):
    # Bubble (rounded rectangle)
    pygame.draw.ellipse(surface, WHITE, (x, y, 240, 50)) 
    pygame.draw.polygon(surface, WHITE, [(x+10, y+40), (x-10, y+60), (x+30, y+45)])
    pygame.draw.ellipse(surface, BLACK, (x, y, 240, 50), 2)
    pygame.draw.polygon(surface, BLACK, [(x+10, y+40), (x-10, y+60), (x+30, y+45)], 2)
    # Text
    font = pygame.font.SysFont(None, 36, bold=True)
    text_surf = font.render(text, True, BLACK)
    surface.blit(text_surf, (x+25, y+12))

running = True
while running:
    screen.fill(BG)
    draw_goose(screen, 120, 140)
    draw_text_bubble(screen, 250, 90, "gurt gurt sybau")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()