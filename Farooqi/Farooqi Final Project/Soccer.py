import pygame
import sys
import os
import random

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Soccer")
clock = pygame.time.Clock()

# --- Colors ---
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
GOAL_COLOR = (200, 200, 200)
YELLOW = (255, 215, 0)

# --- Game Settings ---
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 60
PLAYER_SPEED = 6
BALL_RADIUS = 18
BALL_SPEED = 7
NET_WIDTH, NET_HEIGHT = 10, 120

# --- Fonts ---
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)

# --- Sounds ---
bounce_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "bounce.mp3"))
goal_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "goal.mp3"))

# --- Helper Functions ---
def main_menu():
    menu_font = pygame.font.SysFont(None, 72)
    info_font = pygame.font.SysFont(None, 36)
    while True:
        screen.fill(GREEN)
        title = menu_font.render("Pygame Soccer", True, WHITE)
        play_text = info_font.render("Press SPACE to Start", True, WHITE)
        quit_text = info_font.render("Press ESC to Quit", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
        screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2 - 20))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def get_name(prompt):
    name = ""
    input_font = pygame.font.SysFont(None, 48)
    while True:
        screen.fill(GREEN)
        prompt_surf = input_font.render(prompt, True, BLACK)
        screen.blit(prompt_surf, (WIDTH//2 - prompt_surf.get_width()//2, HEIGHT//2 - 60))
        name_surf = input_font.render(name, True, WHITE)
        screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and (event.unicode.isalnum() or event.unicode == " "):
                    name += event.unicode

def reset_positions():
    global player1_rect, player2_rect, ball_pos, ball_vel, last_hit
    player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball_pos = [WIDTH//2, HEIGHT//2]
    direction = random.choice([-1, 1])
    ball_vel = [BALL_SPEED * direction, BALL_SPEED * random.choice([-1, 1])]
    last_hit = None

def wait_for_space(goal_text):
    # Show goal message and wait for space to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        # Draw overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        msg = font.render(goal_text, True, YELLOW)
        instr = small_font.render("Press SPACE for next round", True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 + 30))
        pygame.display.flip()
        clock.tick(60)

# --- Main Menu & Names ---
main_menu()
player1_name = get_name("Enter name for Player 1 (WASD):")
player2_name = get_name("Enter name for Player 2 (Arrows):")

# --- Ball Image ---
ball_image_path = os.path.join(os.path.dirname(__file__), "ball.png")
ball_img_raw = pygame.image.load(ball_image_path).convert_alpha()
ball_img = pygame.transform.smoothscale(ball_img_raw, (BALL_RADIUS*2, BALL_RADIUS*2))

# --- Game State ---
score1, score2 = 0, 0

# Initialize player rectangles and ball state before main loop
player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [BALL_SPEED, BALL_SPEED]
last_hit = None

reset_positions()

# --- Main Game Loop ---
running = True
while running:
    screen.fill(GREEN)

    # Draw field
    pygame.draw.rect(screen, WHITE, (WIDTH//2-3, 0, 6, HEIGHT))
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 80, 4)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 8)
    left_net = pygame.Rect(0, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)
    right_net = pygame.Rect(WIDTH - NET_WIDTH, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)
    pygame.draw.rect(screen, GOAL_COLOR, left_net)
    pygame.draw.rect(screen, GOAL_COLOR, right_net)

    # Draw players and names
    pygame.draw.rect(screen, RED, player1_rect)
    pygame.draw.rect(screen, BLUE, player2_rect)
    screen.blit(small_font.render(player1_name, True, RED), (player1_rect.x, player1_rect.y - 25))
    screen.blit(small_font.render(player2_name, True, BLUE), (player2_rect.x, player2_rect.y - 25))

    # Draw ball
    ball_center = (int(ball_pos[0]), int(ball_pos[1]))
    ball_rect_img = ball_img.get_rect(center=ball_center)
    screen.blit(ball_img, ball_rect_img)

    # Draw scoreboard and timer
    screen.blit(font.render(f"{score1}   :   {score2}", True, WHITE), (WIDTH//2 - 60, 20))
    elapsed_time = pygame.time.get_ticks() // 1000
    screen.blit(small_font.render(f"{elapsed_time//60}:{elapsed_time%60:02d}", True, WHITE), (20, 20))

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_positions()
                score1 = score2 = 0

    # --- Player Controls ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_rect.top > 0:
        player1_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1_rect.bottom < HEIGHT:
        player1_rect.y += PLAYER_SPEED
    if keys[pygame.K_a] and player1_rect.left > 0:
        player1_rect.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player1_rect.right < WIDTH//2 - 10:
        player1_rect.x += PLAYER_SPEED
    if keys[pygame.K_UP] and player2_rect.top > 0:
        player2_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2_rect.bottom < HEIGHT:
        player2_rect.y += PLAYER_SPEED
    if keys[pygame.K_LEFT] and player2_rect.left > WIDTH//2 + 10:
        player2_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player2_rect.right < WIDTH:
        player2_rect.x += PLAYER_SPEED

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # Ensure ball position remains integers for pygame.Rect compatibility
    ball_pos[0] = int(ball_pos[0])
    ball_pos[1] = int(ball_pos[1])

    # Define ball_rect for collision detection
    ball_rect = pygame.Rect(
        int(ball_pos[0] - BALL_RADIUS),
        int(ball_pos[1] - BALL_RADIUS),
        BALL_RADIUS * 2,
        BALL_RADIUS * 2
    )

    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_pos[1] = BALL_RADIUS
        ball_vel[1] = abs(int(ball_vel[1]))
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_pos[1] = HEIGHT - BALL_RADIUS
        ball_vel[1] = -abs(int(ball_vel[1]))
    if ball_rect.colliderect(player1_rect) and last_hit != "p1":
        ball_pos[0] = player1_rect.right + BALL_RADIUS
        ball_vel[0] = abs(int(ball_vel[0]))
        offset = (ball_pos[1] - player1_rect.centery) / (PLAYER_HEIGHT/2)
        ball_vel[1] = int(BALL_SPEED * offset)
        bounce_sound.play()
        last_hit = "p1"
    elif ball_rect.colliderect(player2_rect) and last_hit != "p2":
        ball_pos[0] = player2_rect.left - BALL_RADIUS
        ball_vel[0] = -abs(int(ball_vel[0]))
        offset = (ball_pos[1] - player2_rect.centery) / (PLAYER_HEIGHT/2)
        ball_vel[1] = int(BALL_SPEED * offset)
        bounce_sound.play()
        last_hit = "p2"
    elif not (ball_rect.colliderect(player1_rect) or ball_rect.colliderect(player2_rect)):
        last_hit = None

    # --- Ball Collision with Nets (Goals) ---
    if left_net.collidepoint(ball_pos[0] - BALL_RADIUS, ball_pos[1]):
        score2 += 1
        goal_sound.play()
        pygame.display.flip()
        wait_for_space(f"GOAL! {player2_name} scores!")
        reset_positions()
        continue
    if right_net.collidepoint(ball_pos[0] + BALL_RADIUS, ball_pos[1]):
        score1 += 1
        goal_sound.play()
        pygame.display.flip()
        wait_for_space(f"GOAL! {player1_name} scores!")
        reset_positions()
        continue

    # --- Ball Collision with Left/Right Walls ---
    if ball_pos[0] - BALL_RADIUS <= 0:
        ball_pos[0] = BALL_RADIUS
        ball_vel[0] = abs(ball_vel[0])
    if ball_pos[0] + BALL_RADIUS >= WIDTH:
        ball_pos[0] = WIDTH - BALL_RADIUS
        ball_vel[0] = -abs(ball_vel[0])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()