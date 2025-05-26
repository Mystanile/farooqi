import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Soccer")

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
GOAL_COLOR = (200, 200, 200)

# Player settings
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 60
PLAYER_SPEED = 6

# Ball settings
BALL_RADIUS = 18
BALL_SPEED = 7

# Net settings
NET_WIDTH = 10
NET_HEIGHT = 120

# Score
score1 = 0
score2 = 0

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)

# Name Input
def get_name(prompt):
    name = ""
    input_active = True
    input_font = pygame.font.SysFont(None, 48)
    while input_active:
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
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and (event.unicode.isalnum() or event.unicode == " "):
                    name += event.unicode
    return name.strip()

# Get player names
player1_name = get_name("Enter name for Player 1 (WASD):")
player2_name = get_name("Enter name for Player 2 (Arrows):")

# Load and scale ball image to fully fill the ball (no gaps)
ball_image_path = os.path.join(os.path.dirname(__file__), "ball.png")
ball_img_raw = pygame.image.load(ball_image_path).convert_alpha()
# Create a new surface with a white background
ball_img = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2), pygame.SRCALPHA)
pygame.draw.circle(ball_img, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
# Stretch the image to fill the entire ball area
ball_img_scaled = pygame.transform.smoothscale(ball_img_raw, (BALL_RADIUS*2, BALL_RADIUS*2))
ball_img.blit(ball_img_scaled, (0, 0))

# Initialize player and ball positions
def reset_positions():
    global player1_rect, player2_rect, ball_pos, ball_vel
    player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball_pos = [WIDTH//2, HEIGHT//2]
    ball_vel = [BALL_SPEED, BALL_SPEED]

player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
reset_positions()

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(GREEN)

    # Draw field lines
    pygame.draw.rect(screen, WHITE, (WIDTH//2-3, 0, 6, HEIGHT))
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 80, 4)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 8)

    # Draw nets
    left_net = pygame.Rect(0, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)
    right_net = pygame.Rect(WIDTH - NET_WIDTH, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)
    pygame.draw.rect(screen, GOAL_COLOR, left_net)
    pygame.draw.rect(screen, GOAL_COLOR, right_net)

    # Draw players as thin rectangles
    pygame.draw.rect(screen, RED, player1_rect)
    pygame.draw.rect(screen, BLUE, player2_rect)
    # Player labels (use entered names)
    label1 = small_font.render(player1_name, True, BLACK)
    label2 = small_font.render(player2_name, True, BLACK)
    screen.blit(label1, (player1_rect.x, player1_rect.y - 25))
    screen.blit(label2, (player2_rect.x, player2_rect.y - 25))

    # Draw ball with white background circle, then the image on top
    ball_center = (int(ball_pos[0]), int(ball_pos[1]))
    ball_rect = ball_img.get_rect(center=ball_center)
    screen.blit(ball_img, ball_rect)

    # Draw scoreboard
    score_text = font.render(f"{score1}   :   {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_positions()
                score1 = 0
                score2 = 0

    # Player 1 controls (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_rect.top > 0:
        player1_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1_rect.bottom < HEIGHT:
        player1_rect.y += PLAYER_SPEED
    if keys[pygame.K_a] and player1_rect.left > 0:
        player1_rect.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player1_rect.right < WIDTH//2 - 10:
        player1_rect.x += PLAYER_SPEED

    # Player 2 controls (Arrow keys)
    if keys[pygame.K_UP] and player2_rect.top > 0:
        player2_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2_rect.bottom < HEIGHT:
        player2_rect.y += PLAYER_SPEED
    if keys[pygame.K_LEFT] and player2_rect.left > WIDTH//2 + 10:
        player2_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player2_rect.right < WIDTH:
        player2_rect.x += PLAYER_SPEED

    # Ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collision with top/bottom
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # Ball collision with players
    ball_rect = pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
    if ball_rect.colliderect(player1_rect):
        ball_vel[0] = abs(ball_vel[0])
        ball_vel[1] += (ball_pos[1] - player1_rect.centery) // 8
    if ball_rect.colliderect(player2_rect):
        ball_vel[0] = -abs(ball_vel[0])
        ball_vel[1] += (ball_pos[1] - player2_rect.centery) // 8

    # Ball collision with left net (goal for player 2)
    if left_net.collidepoint(ball_pos[0] - BALL_RADIUS, ball_pos[1]):
        score2 += 1
        reset_positions()
        pygame.display.flip()
        pygame.time.delay(700)
        continue

    # Ball collision with right net (goal for player 1)
    if right_net.collidepoint(ball_pos[0] + BALL_RADIUS, ball_pos[1]):
        score1 += 1
        reset_positions()
        pygame.display.flip()
        pygame.time.delay(700)
        continue

    # Ball collision with left/right walls (not net)
    if ball_pos[0] - BALL_RADIUS <= 0:
        ball_vel[0] = abs(ball_vel[0])
    if ball_pos[0] + BALL_RADIUS >= WIDTH:
        ball_vel[0] = -abs(ball_vel[0])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()