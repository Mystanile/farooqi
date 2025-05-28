import pygame  # Import the pygame library for game development
import sys     # Import sys for system-specific parameters and functions
import os      # Import os for file path operations

# Initialize Pygame
pygame.init()  # Initialize all imported pygame modules

# Screen settings
WIDTH, HEIGHT = 900, 500  # Set the width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Pygame Soccer")  # Set the window title

# Colors
GREEN = (34, 139, 34)      # Define the color green for the field
WHITE = (255, 255, 255)    # Define the color white
RED = (220, 20, 60)        # Define the color red for player 1
BLUE = (30, 144, 255)      # Define the color blue for player 2
BLACK = (0, 0, 0)          # Define the color black
YELLOW = (255, 215, 0)     # Define the color yellow (not used here)
GOAL_COLOR = (200, 200, 200)  # Define the color for the goal/net

# Player settings
PLAYER_WIDTH = 20          # Set the width of each player rectangle
PLAYER_HEIGHT = 60         # Set the height of each player rectangle
PLAYER_SPEED = 6           # Set the speed at which players move

# Ball settings
BALL_RADIUS = 18           # Set the radius of the ball
BALL_SPEED = 7             # Set the initial speed of the ball

# Net settings
NET_WIDTH = 10             # Set the width of the goal/net
NET_HEIGHT = 120           # Set the height of the goal/net

# Score
score1 = 0                 # Initialize player 1's score to 0
score2 = 0                 # Initialize player 2's score to 0

# Fonts
font = pygame.font.SysFont(None, 48)      # Create a font object for large text
small_font = pygame.font.SysFont(None, 28)  # Create a font object for small text

# Name Input
def get_name(prompt):  # Function to get a player's name with a prompt
    name = ""  # Start with an empty name
    input_active = True  # Flag to keep the input loop running
    input_font = pygame.font.SysFont(None, 48)  # Font for input text
    while input_active:  # Loop until the user presses Enter
        screen.fill(GREEN)  # Fill the screen with green
        prompt_surf = input_font.render(prompt, True, BLACK)  # Render the prompt text
        screen.blit(prompt_surf, (WIDTH//2 - prompt_surf.get_width()//2, HEIGHT//2 - 60))  # Draw the prompt centered
        name_surf = input_font.render(name, True, WHITE)  # Render the current name input
        screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, HEIGHT//2))  # Draw the name input centered
        pygame.display.flip()  # Update the display
        for event in pygame.event.get():  # Process events
            if event.type == pygame.QUIT:  # If the window is closed
                pygame.quit(); sys.exit()  # Quit the game
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_RETURN and name.strip():  # If Enter is pressed and name is not empty
                    input_active = False  # Exit the input loop
                elif event.key == pygame.K_BACKSPACE:  # If Backspace is pressed
                    name = name[:-1]  # Remove the last character
                elif len(name) < 12 and (event.unicode.isalnum() or event.unicode == " "):  # If input is valid
                    name += event.unicode  # Add the character to the name
    return name.strip()  # Return the entered name without leading/trailing spaces

# Get player names
player1_name = get_name("Enter name for Player 1 (WASD):")  # Prompt for player 1's name
player2_name = get_name("Enter name for Player 2 (Arrows):")  # Prompt for player 2's name

# Load and scale ball image to fully fill the ball (no gaps)
ball_image_path = os.path.join(os.path.dirname(__file__), "ball.png")  # Get the path to ball.png
ball_img_raw = pygame.image.load(ball_image_path).convert_alpha()  # Load the ball image with transparency
ball_img = pygame.transform.smoothscale(ball_img_raw, (BALL_RADIUS*2, BALL_RADIUS*2))  # Scale the image to fit the ball

# Initialize player and ball positions
def reset_positions():  # Function to reset player and ball positions
    global player1_rect, player2_rect, ball_pos, ball_vel  # Use global variables
    player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Player 1's rectangle
    player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Player 2's rectangle
    ball_pos = [WIDTH//2, HEIGHT//2]  # Ball position at center
    ball_vel = [BALL_SPEED, BALL_SPEED]  # Ball velocity

player1_rect = pygame.Rect(60, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Initial player 1 rectangle
player2_rect = pygame.Rect(WIDTH-60-PLAYER_WIDTH, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Initial player 2 rectangle
reset_positions()  # Set initial positions

clock = pygame.time.Clock()  # Create a clock object to control FPS

running = True  # Main loop flag
while running:  # Main game loop
    screen.fill(GREEN)  # Fill the screen with green (field)

    # Draw field lines
    pygame.draw.rect(screen, WHITE, (WIDTH//2-3, 0, 6, HEIGHT))  # Draw the center line
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 80, 4)  # Draw the center circle
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 8)  # Draw the center spot

    # Draw nets
    left_net = pygame.Rect(0, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)  # Left goal rectangle
    right_net = pygame.Rect(WIDTH - NET_WIDTH, HEIGHT//2 - NET_HEIGHT//2, NET_WIDTH, NET_HEIGHT)  # Right goal rectangle
    pygame.draw.rect(screen, GOAL_COLOR, left_net)  # Draw left goal
    pygame.draw.rect(screen, GOAL_COLOR, right_net)  # Draw right goal

    # Draw players as thin rectangles
    pygame.draw.rect(screen, RED, player1_rect)  # Draw player 1
    pygame.draw.rect(screen, BLUE, player2_rect)  # Draw player 2
    # Player labels (use entered names)
    label1 = small_font.render(player1_name, True, RED)  # Render player 1's name in red
    label2 = small_font.render(player2_name, True, BLUE)  # Render player 2's name in blue
    screen.blit(label1, (player1_rect.x, player1_rect.y - 25))  # Draw player 1's name above their rectangle
    screen.blit(label2, (player2_rect.x, player2_rect.y - 25))  # Draw player 2's name above their rectangle

    # Draw ball with white background circle, then the image on top
    ball_center = (int(ball_pos[0]), int(ball_pos[1]))  # Get the center position of the ball
    ball_rect = ball_img.get_rect(center=ball_center)  # Get the rectangle for the ball image centered
    screen.blit(ball_img, ball_rect)  # Draw the ball image

    # Draw scoreboard
    score_text = font.render(f"{score1}   :   {score2}", True, WHITE)  # Render the score text
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))  # Draw the score at the top center

    #Draw the elapsed time in top left corner in the format "0:00"
    elapsed_time = pygame.time.get_ticks() // 1000  # Get elapsed time in seconds
    minutes = elapsed_time // 60  # Calculate minutes
    seconds = elapsed_time % 60   # Calculate seconds
    time_text = small_font.render(f"{minutes}:{seconds:02d}", True, WHITE)  # Render the time text
    screen.blit(time_text, (20, 20))  # Draw the time at the top left

    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # If the window is closed
            running = False  # Exit the main loop
        elif event.type == pygame.KEYDOWN:  # If a key is pressed
            if event.key == pygame.K_r:  # If 'R' is pressed
                reset_positions()  # Reset positions
                score1 = 0  # Reset player 1's score
                score2 = 0  # Reset player 2's score

    # Player 1 controls (WASD)
    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
    if keys[pygame.K_w] and player1_rect.top > 0:  # Move up if 'W' is pressed and not at the top
        player1_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1_rect.bottom < HEIGHT:  # Move down if 'S' is pressed and not at the bottom
        player1_rect.y += PLAYER_SPEED
    if keys[pygame.K_a] and player1_rect.left > 0:  # Move left if 'A' is pressed and not at the left edge
        player1_rect.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player1_rect.right < WIDTH//2 - 10:  # Move right if 'D' is pressed and not past center
        player1_rect.x += PLAYER_SPEED

    # Player 2 controls (Arrow keys)
    if keys[pygame.K_UP] and player2_rect.top > 0:  # Move up if up arrow is pressed
        player2_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2_rect.bottom < HEIGHT:  # Move down if down arrow is pressed
        player2_rect.y += PLAYER_SPEED
    if keys[pygame.K_LEFT] and player2_rect.left > WIDTH//2 + 10:  # Move left if left arrow is pressed
        player2_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player2_rect.right < WIDTH:  # Move right if right arrow is pressed
        player2_rect.x += PLAYER_SPEED

    # Ball movement
    ball_pos[0] += ball_vel[0]  # Update ball's x position
    ball_pos[1] += ball_vel[1]  # Update ball's y position

    # Ball collision with top/bottom
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:  # If ball hits top or bottom
        ball_vel[1] = -ball_vel[1]  # Reverse y velocity

    # Ball collision with players
    ball_rect = pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)  # Ball's rectangle
    if ball_rect.colliderect(player1_rect):  # If ball collides with player 1
        ball_vel[0] = abs(ball_vel[0])  # Ensure ball moves right
        ball_vel[1] += (ball_pos[1] - player1_rect.centery) // 8  # Add some vertical "spin"
    if ball_rect.colliderect(player2_rect):  # If ball collides with player 2
        ball_vel[0] = -abs(ball_vel[0])  # Ensure ball moves left
        ball_vel[1] += (ball_pos[1] - player2_rect.centery) // 8  # Add some vertical "spin"

    # Ball collision with left net (goal for player 2)
    if left_net.collidepoint(ball_pos[0] - BALL_RADIUS, ball_pos[1]):  # If ball enters left goal
        score2 += 1  # Player 2 scores
        reset_positions()  # Reset positions
        pygame.display.flip()  # Update display
        pygame.time.delay(700)  # Pause for 0.7 seconds
        continue  # Skip the rest of the loop

    # Ball collision with right net (goal for player 1)
    if right_net.collidepoint(ball_pos[0] + BALL_RADIUS, ball_pos[1]):  # If ball enters right goal
        score1 += 1  # Player 1 scores
        reset_positions()  # Reset positions
        pygame.display.flip()  # Update display
        pygame.time.delay(700)  # Pause for 0.7 seconds
        continue  # Skip the rest of the loop

    # Ball collision with left/right walls (not net)
    if ball_pos[0] - BALL_RADIUS <= 0:  # If ball hits left wall
        ball_vel[0] = abs(ball_vel[0])  # Move ball right
    if ball_pos[0] + BALL_RADIUS >= WIDTH:  # If ball hits right wall
        ball_vel[0] = -abs(ball_vel[0])  # Move ball left

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()  # Quit pygame
sys.exit()     # Exit the program