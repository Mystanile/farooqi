import pygame
import sys
import os

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROW_COLORS = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 128, 255),  # Blue
    (128, 0, 255),  # Purple
]

# --- Paddle ---
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 18
PADDLE_SPEED = 8
paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# --- Ball ---
BALL_RADIUS = 16
BALL_SPEED = 6
ball_image_path = os.path.join(os.path.dirname(__file__), "ball.png")
ball_img_raw = pygame.image.load(ball_image_path).convert_alpha()
ball_img = pygame.transform.smoothscale(ball_img_raw, (BALL_RADIUS*2, BALL_RADIUS*2))
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [BALL_SPEED, -BALL_SPEED]

# --- Bricks ---
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_rect = pygame.Rect(col*BRICK_WIDTH+2, row*BRICK_HEIGHT+2, BRICK_WIDTH-4, BRICK_HEIGHT-4)
        bricks.append((brick_rect, ROW_COLORS[row % len(ROW_COLORS)]))

# --- Score ---
score = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, paddle)

    # Draw ball (centered)
    ball_center = (int(ball_pos[0]), int(ball_pos[1]))
    ball_rect = ball_img.get_rect(center=ball_center)
    screen.blit(ball_img, ball_rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 10))

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Paddle movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    # --- Ball movement ---
    ball_pos[0] += ball_vel[0] #type: ignore
    ball_pos[1] += ball_vel[1]

    # --- Ball collision with walls ---
    if ball_pos[0] - BALL_RADIUS <= 0 or ball_pos[0] + BALL_RADIUS >= WIDTH:
        ball_vel[0] = -ball_vel[0] #type: ignore
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        # Reset ball and paddle
        ball_pos = [WIDTH//2, HEIGHT//2]
        ball_vel = [BALL_SPEED, -BALL_SPEED]
        paddle.x = WIDTH//2 - PADDLE_WIDTH//2

    # --- Ball collision with paddle ---
    if paddle.colliderect(pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)):
        ball_vel[1] = -abs(ball_vel[1])
        # Add some "english" based on where it hit the paddle
        offset = (ball_pos[0] - paddle.centerx) / (PADDLE_WIDTH//2)
        ball_vel[0] += offset * 2 #type: ignore
        # Clamp ball speed
        ball_vel[0] = max(-BALL_SPEED, min(BALL_SPEED, ball_vel[0])) #type: ignore

    # --- Ball collision with bricks ---
    hit_index = None
    for i, (brick, color) in enumerate(bricks):
        if brick.colliderect(pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)):
            hit_index = i
            break
    if hit_index is not None:
        hit_brick, _ = bricks.pop(hit_index)
        score += 10
        # Determine collision side
        if abs(ball_pos[1] - hit_brick.top) < 10 or abs(ball_pos[1] - hit_brick.bottom) < 10:
            ball_vel[1] = -ball_vel[1]
        else:
            ball_vel[0] = -ball_vel[0] #type: ignore

    # --- Win condition ---
    if not bricks:
        win_text = font.render("You Win! Press ESC to quit.", True, (255,255,0))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            clock.tick(30)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()