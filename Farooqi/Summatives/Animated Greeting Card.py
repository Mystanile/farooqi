import pygame
import sys
import random
import os

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Birthday!")
clock = pygame.time.Clock()

# --- Colors ---
BG_TOP = (120, 180, 255)      # Lighter blue for gradient
BG_BOTTOM = (30, 60, 120)     # Darker blue for gradient
WHITE = (255, 255, 255)
BALLOON_COLORS = [
    ((255, 80, 80), (200, 0, 0)),      # Red (main, shadow)
    ((80, 255, 120), (0, 180, 60)),    # Green
    ((255, 255, 120), (200, 200, 0)),  # Yellow
    ((255, 120, 220), (180, 0, 120)),  # Pink
    ((120, 220, 255), (0, 120, 180)),  # Blue
    ((255, 180, 80), (200, 120, 0)),   # Orange
]
CONFETTI_COLORS = [
    (255,0,0), (0,255,0), (0,0,255), (255,255,0),
    (255,0,255), (0,255,255), (255,255,255)
]

# --- Load Images ---
cake_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "cake.png"))
cake_img = pygame.transform.scale(cake_img, (120, 100))
cake_rect = cake_img.get_rect(midbottom=(WIDTH//2, HEIGHT-20))

# --- Balloons ---
class Balloon:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = HEIGHT + random.randint(0, 200)
        self.colors = random.choice(BALLOON_COLORS)
        self.speed = random.uniform(1, 2.5)
        self.size = random.randint(38, 54)
        self.offset = random.randint(-10, 10)
    def update(self):
        self.y -= self.speed
        if self.y < -self.size*1.3:
            self.__init__()
    def draw(self, surf):
        main, shadow = self.colors
        # Balloon shadow (bottom right, slightly offset)
        balloon_rect = pygame.Rect(self.x+self.offset+6, self.y+6, self.size, int(self.size*1.3))
        pygame.draw.ellipse(surf, shadow, balloon_rect)
        # Balloon main
        balloon_rect_main = pygame.Rect(self.x+self.offset, self.y, self.size, int(self.size*1.3))
        pygame.draw.ellipse(surf, main, balloon_rect_main)
        # Balloon highlight (top left)
        highlight_rect = pygame.Rect(self.x+self.offset+8, self.y+10, self.size//4, self.size//5)
        pygame.draw.ellipse(surf, WHITE, highlight_rect)
        # String
        pygame.draw.line(surf, (120,80,40), (self.x+self.offset+self.size//2, self.y+self.size*1.3),
                         (self.x+self.offset+self.size//2, self.y+self.size*1.7), 2)

balloons = [Balloon() for _ in range(8)]

# --- Confetti ---
class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.color = random.choice(CONFETTI_COLORS)
        self.angle = random.randint(0, 360)
        self.size = random.randint(4, 10)
        self.speed = random.uniform(2, 5)
    def update(self):
        self.y += self.speed
        self.angle += random.randint(-10, 10)
        if self.y > HEIGHT:
            self.__init__()
    def draw(self, surf):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surf, self.color, rect)

confetti = [Confetti() for _ in range(40)]

# --- Greeting Text ---
greeting = "Happy Birthday!"
typed = ""
type_timer = 0
type_index = 0
text_color = (255,255,255)

# --- Candle State ---
candle_on = True

# --- Sound (Optional) ---
pygame.mixer.music.load("birthday_song.mp3")

def draw_gradient_background(surface, top_color, bottom_color):
    """Draw a vertical gradient background."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# --- Main Loop ---
running = True
while running:
    draw_gradient_background(screen, BG_TOP, BG_BOTTOM)

    # Draw confetti
    for c in confetti:
        c.update()
        c.draw(screen)

    # Draw balloons
    for b in balloons:
        b.update()
        b.draw(screen)

    # Draw table under the cake
    table_color = (180, 120, 60)  # Brown
    table_rect = pygame.Rect(cake_rect.left - 40, cake_rect.bottom - 10, cake_rect.width + 80, 40)
    pygame.draw.rect(screen, table_color, table_rect, border_radius=12)


    # Draw cake
    screen.blit(cake_img, cake_rect)

    # Draw candle (simple yellow rectangle)
    if candle_on:
        pygame.draw.rect(screen, (255,255,100), (cake_rect.centerx-5, cake_rect.top-30, 10, 30))
        pygame.draw.ellipse(screen, (255,200,0), (cake_rect.centerx-8, cake_rect.top-38, 16, 16))

    # Animated greeting text (typing effect)
    if type_index < len(greeting):
        type_timer += 1
        if type_timer % 5 == 0:
            typed += greeting[type_index]
            type_index += 1
    font = pygame.font.SysFont("comicsansms", 48, bold=True)
    text_surface = font.render(typed, True, text_color)
    screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 60))

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Play music on spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play()
        # Mouse movement changes text color
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            text_color = (mx % 256, my % 256, (mx+my) % 256)
        # Click on cake blows out candle
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cake_rect.collidepoint(event.pos):
                candle_on = not candle_on

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()