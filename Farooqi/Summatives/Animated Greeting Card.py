import pygame                 # Import the pygame library for graphics, sound, and input
import sys                    # Import sys for system exit
import random                 # Import random for random positions/colors
import os                     # Import os for file path handling
import math                   # Import math for trigonometric functions

# --- Setup ---
pygame.init()                 # Initialize all imported pygame modules
WIDTH, HEIGHT = 800, 600      # Set the width and height of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the main display surface
pygame.display.set_caption("Happy Birthday!")      # Set the window title
clock = pygame.time.Clock()    # Create a clock object to control the frame rate

# --- Colors ---
BG_TOP = (120, 180, 255)      # Lighter blue for gradient background (top)
BG_BOTTOM = (30, 60, 120)     # Darker blue for gradient background (bottom)
WHITE = (255, 255, 255)       # White color for highlights and text

# Balloon colors: each is a tuple of (main color, shadow color)
BALLOON_COLORS = [
    ((255, 80, 80), (200, 0, 0)),      # Red (main, shadow)
    ((80, 255, 120), (0, 180, 60)),    # Green
    ((255, 255, 120), (200, 200, 0)),  # Yellow
    ((255, 120, 220), (180, 0, 120)),  # Pink
    ((120, 220, 255), (0, 120, 180)),  # Blue
    ((255, 180, 80), (200, 120, 0)),   # Orange
]
# Confetti colors
CONFETTI_COLORS = [
    (255,0,0), (0,255,0), (0,0,255), (255,255,0),
    (255,0,255), (0,255,255), (255,255,255)
]

# --- Load Images ---
# Load the cake image from the same directory as the script
cake_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "cake.png"))
cake_img = pygame.transform.scale(cake_img, (120, 100))  # Scale the cake image to 120x100 pixels
cake_rect = cake_img.get_rect(midbottom=(WIDTH//2, HEIGHT-20))  # Position the cake at the bottom center

# --- Balloons ---
class Balloon:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)  # Random horizontal position
        self.y = HEIGHT + random.randint(0, 200)  # Start below the screen
        self.colors = random.choice(BALLOON_COLORS)  # Random color (main, shadow)
        self.speed = random.uniform(1, 2.5)         # Random upward speed
        self.size = random.randint(38, 54)          # Random balloon size
        self.offset = random.randint(-10, 10)       # Slight horizontal offset for variety
    def update(self):
        self.y -= self.speed                        # Move the balloon up
        if self.y < -self.size*1.3:                 # If balloon is above the screen, reset it
            self.__init__()
    def draw(self, surf):
        main, shadow = self.colors
        # Draw the shadow (slightly offset)
        balloon_rect = pygame.Rect(self.x+self.offset+6, self.y+6, self.size, int(self.size*1.3))
        pygame.draw.ellipse(surf, shadow, balloon_rect)
        # Draw the main balloon
        balloon_rect_main = pygame.Rect(self.x+self.offset, self.y, self.size, int(self.size*1.3))
        pygame.draw.ellipse(surf, main, balloon_rect_main)
        # Draw the highlight
        highlight_rect = pygame.Rect(self.x+self.offset+8, self.y+10, self.size//4, self.size//5)
        pygame.draw.ellipse(surf, WHITE, highlight_rect)
        # Draw the string
        pygame.draw.line(surf, (120,80,40), (self.x+self.offset+self.size//2, self.y+self.size*1.3),
                         (self.x+self.offset+self.size//2, self.y+self.size*1.7), 2)

balloons = [Balloon() for _ in range(8)]  # Create a list of 8 balloons

# --- Confetti ---
class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)           # Random horizontal position
        self.y = random.randint(-HEIGHT, 0)         # Random vertical start (above screen)
        self.color = random.choice(CONFETTI_COLORS) # Random color
        self.angle = random.randint(0, 360)         # Random angle (not used for drawing)
        self.size = random.randint(4, 10)           # Random size
        self.speed = random.uniform(2, 5)           # Random falling speed
    def update(self):
        self.y += self.speed                        # Move confetti down
        self.angle += random.randint(-10, 10)       # Randomly change angle (not used)
        if self.y > HEIGHT:                         # If below screen, reset
            self.__init__()
    def draw(self, surf):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surf, self.color, rect)    # Draw confetti as a rectangle

confetti = [Confetti() for _ in range(40)]         # Create a list of 40 confetti pieces

# --- Animated Character (Waving) ---
class WavingCharacter:
    def __init__(self, x, y):
        self.x = x                                 # Character's top-left x position
        self.y = y                                 # Character's top-left y position
        self.arm_angle = 0                         # Current waving angle
        self.arm_direction = 1                     # 1 = up, -1 = down
        self.arm_speed = 2                         # How fast the arm waves

    def update(self):
        # Animate the arm waving up and down between -30 and 30 degrees
        self.arm_angle += self.arm_direction * self.arm_speed
        if self.arm_angle > 30:
            self.arm_angle = 30
            self.arm_direction = -1
        elif self.arm_angle < -30:
            self.arm_angle = -30
            self.arm_direction = 1

    def draw(self, surf):
        # Body
        body_rect = pygame.Rect(self.x, self.y + 40, 40, 60)
        pygame.draw.ellipse(surf, (255, 220, 180), body_rect)  # body fill
        pygame.draw.ellipse(surf, (80, 40, 20), body_rect, 3)  # body outline

        # Head
        head_center = (self.x + 20, self.y + 25)
        pygame.draw.circle(surf, (255, 230, 200), head_center, 22)  # head fill
        pygame.draw.circle(surf, (80, 40, 20), head_center, 22, 3)  # head outline

        # Eyes
        pygame.draw.circle(surf, (0, 0, 0), (self.x + 13, self.y + 25), 3)
        pygame.draw.circle(surf, (0, 0, 0), (self.x + 27, self.y + 25), 3)

        # Smile
        pygame.draw.arc(surf, (120, 80, 40), (self.x + 10, self.y + 30, 20, 10), 3.5, 6, 2)

        # Left arm (waving, attached to side of body, waving at an angle)
        arm_length = 38
        arm_base_x = self.x
        arm_base_y = self.y + 60
        angle_deg = -135 + self.arm_angle
        angle_rad = angle_deg * math.pi / 180
        hand_x = int(arm_base_x + arm_length * math.cos(angle_rad))
        hand_y = int(arm_base_y + arm_length * math.sin(angle_rad))
        # Draw outline first (thicker, under the fill)
        pygame.draw.line(surf, (80, 40, 20), (arm_base_x, arm_base_y), (hand_x, hand_y), 10)
        pygame.draw.line(surf, (255, 220, 180), (arm_base_x, arm_base_y), (hand_x, hand_y), 6)

        # Right arm (static, attached to right side of body)
        right_arm_base_x = self.x + 40
        right_arm_base_y = self.y + 60
        pygame.draw.line(surf, (80, 40, 20), (right_arm_base_x, right_arm_base_y), (right_arm_base_x + 30, right_arm_base_y + 30), 10)
        pygame.draw.line(surf, (255, 220, 180), (right_arm_base_x, right_arm_base_y), (right_arm_base_x + 30, right_arm_base_y + 30), 6)

        # Legs
        # Left leg
        pygame.draw.line(surf, (80, 40, 20), (self.x + 10, self.y + 100), (self.x + 10, self.y + 130), 9)
        pygame.draw.line(surf, (120, 80, 40), (self.x + 10, self.y + 100), (self.x + 10, self.y + 130), 5)
        # Right leg
        pygame.draw.line(surf, (80, 40, 20), (self.x + 30, self.y + 100), (self.x + 30, self.y + 130), 9)
        pygame.draw.line(surf, (120, 80, 40), (self.x + 30, self.y + 100), (self.x + 30, self.y + 130), 5)
character = WavingCharacter(70, 180)  # Create the waving character at position (70, 180)

# --- Greeting Text ---
greeting = "Happy Birthday!"          # The greeting message
typed = ""                            # The part of the message that has appeared
type_timer = 0                        # Timer for typing effect
type_index = 0                        # Current letter index for typing effect
text_color = (255,255,255)            # Initial text color

# --- Candle State ---
candle_on = True                      # Whether the candle is lit

# --- Sound (Optional) ---
pygame.mixer.music.load("birthday_song.mp3")  # Load the birthday song

def draw_gradient_background(surface, top_color, bottom_color):
    """Draw a vertical gradient background."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# --- Opening Screen ---
def opening_screen():
    font_big = pygame.font.SysFont("comicsansms", 38, bold=True)  # Smaller font for better fit
    font_small = pygame.font.SysFont("comicsansms", 28, bold=True)
    # Use the same gradient as the card for consistency
    while True:
        draw_gradient_background(screen, BG_TOP, BG_BOTTOM)
        text = font_big.render("Click me to open your birthday card!", True, (80, 40, 20))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
        pygame.draw.rect(screen, (255, 220, 120), (WIDTH//2 - 120, HEIGHT//2 + 20, 240, 60), border_radius=18)
        click_text = font_small.render("CLICK HERE", True, (120, 80, 40))
        screen.blit(click_text, (WIDTH//2 - click_text.get_width()//2, HEIGHT//2 + 38))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 20, 240, 60).collidepoint(event.pos):
                    return
        pygame.display.flip()
        clock.tick(60)

# --- Card Opening Animation ---
def page_turn_animation():
    # Animate a "page" flipping from left to right
    for i in range(0, WIDTH+1, 32):
        draw_gradient_background(screen, BG_TOP, BG_BOTTOM)
        # Draw the "page" as a white rectangle that rotates open from the left
        page_width = WIDTH - i
        if page_width > 0:
            page_surface = pygame.Surface((page_width, HEIGHT), pygame.SRCALPHA)
            page_surface.fill((245, 245, 230, 255))
            # Simulate a curved shadow on the edge for realism
            shadow_width = min(30, page_width)
            for s in range(shadow_width):
                alpha = int(80 * (1 - s / shadow_width))
                pygame.draw.rect(page_surface, (180, 180, 180, alpha), (page_width - s - 1, 0, 1, HEIGHT))
            screen.blit(page_surface, (i, 0))
        pygame.display.flip()
        pygame.time.delay(18)

# --- Countdown Screen ---
def countdown_screen():
    font = pygame.font.SysFont("comicsansms", 100, bold=True)
    for n in range(3, 0, -1):
        draw_gradient_background(screen, BG_TOP, BG_BOTTOM)
        count_text = font.render(str(n), True, (255, 255, 255))
        screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, HEIGHT//2 - count_text.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(700)

# --- Main Loop ---
def main_card():
    global typed, type_timer, type_index, text_color, candle_on
    running = True
    while running:
        draw_gradient_background(screen, BG_TOP, BG_BOTTOM)

        # Draw animated waving character
        character.update()
        character.draw(screen)

        # Draw confetti
        for c in confetti:
            c.update()
            c.draw(screen)

        # Draw balloons
        for b in balloons:
            b.update()
            b.draw(screen)

        # Draw 3D table under the cake
        table_color_top = (200, 140, 70)    # Lighter brown for top
        table_color_front = (160, 100, 40)  # Darker brown for front
        table_shadow = (110, 70, 30)        # Even darker for shadow

        # Table top (slightly angled ellipse for 3D effect)
        table_top_rect = pygame.Rect(cake_rect.left - 40, cake_rect.bottom - 25, cake_rect.width + 80, 32)
        pygame.draw.ellipse(screen, table_color_top, table_top_rect)

        # Table front (rectangle with shadow for thickness)
        table_front_rect = pygame.Rect(cake_rect.left - 40, cake_rect.bottom - 10, cake_rect.width + 80, 38)
        pygame.draw.rect(screen, table_color_front, table_front_rect, border_radius=12)

        # Table shadow (ellipse at the base)
        shadow_rect = pygame.Rect(cake_rect.left - 30, cake_rect.bottom + 18, cake_rect.width + 60, 18)
        pygame.draw.ellipse(screen, table_shadow, shadow_rect)

        # Draw note on the table
        note_color = (255, 255, 200)
        note_rect = pygame.Rect(cake_rect.centerx - 80, table_front_rect.top + 8, 160, 28)
        pygame.draw.rect(screen, note_color, note_rect, border_radius=8)
        pygame.draw.rect(screen, (180, 180, 120), note_rect, 2, border_radius=8)  # Note border

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

# --- Run the screens in order ---
opening_screen()         # Show the opening screen
countdown_screen()       # Show the countdown
page_turn_animation()    # Show the page turn animation
main_card()              # Show the main card