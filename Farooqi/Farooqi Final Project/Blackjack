import pygame
import sys
import random

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont("arialunicodeMS,arial", 36)  # Use a font that supports Unicode suits
big_font = pygame.font.SysFont("arialunicodeMS,arial", 60)
clock = pygame.time.Clock()

# --- Card Setup ---
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
VALUES = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def hand_value(hand):
    value = sum(VALUES[card[0]] for card in hand)
    # Adjust for Aces
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_hand(hand, x, y, hide_first=False):
    for i, card in enumerate(hand):
        rect = pygame.Rect(x + i*70, y, 60, 90) 
        pygame.draw.rect(screen, (255,255,255), rect)
        pygame.draw.rect(screen, (0,0,0), rect, 2)
        if hide_first and i == 0:
            pygame.draw.rect(screen, (0,0,128), rect)
        else:
            # Color for suits
            color = (200,0,0) if card[1] in ['♥', '♦'] else (0,0,0)
            text = font.render(f"{card[0]}{card[1]}", True, color)
            screen.blit(text, (rect.x+10, rect.y+25))

def show_message(msg, color=(0,0,0)):
    text = big_font.render(msg, True, color)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

# --- Betting System ---
player_money = 1000
current_bet = 100
betting = True

def get_bet():
    global current_bet, betting 
    bet_str = ""
    input_active = True
    while input_active:
        screen.fill((0,128,0))
        prompt = big_font.render("Place your bet:", True, (255,255,255))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 150))
        bet_text = big_font.render(f"${bet_str if bet_str else '0'}", True, (255,255,0))
        screen.blit(bet_text, (WIDTH//2 - bet_text.get_width()//2, 250))
        info = font.render(f"Money: ${player_money}", True, (255,255,255))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 350))
        inst = font.render("Enter amount, Enter to confirm, Backspace to erase", True, (255,255,255))
        screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 420))
        pygame.display.flip() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and bet_str.isdigit() and 1 <= int(bet_str) <= player_money:
                    current_bet = int(bet_str)
                    input_active = False
                    betting = False
                elif event.key == pygame.K_BACKSPACE:
                    bet_str = bet_str[:-1]
                elif event.unicode.isdigit() and len(bet_str) < 6:
                    bet_str += event.unicode

# --- Game State ---
def reset_game():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    return deck, player_hand, dealer_hand, False, False, "" 

deck, player_hand, dealer_hand, player_stand, game_over, result = reset_game()

while True:
    if betting:
        get_bet()
        deck, player_hand, dealer_hand, player_stand, game_over, result = reset_game()

    screen.fill((0,128,0))

    # Centered positions for hands
    player_x = WIDTH//2 - (len(player_hand)*70)//2
    dealer_x = WIDTH//2 - (len(dealer_hand)*70)//2

    # Draw hands in the center
    draw_hand(dealer_hand, dealer_x, HEIGHT//2 - 150, hide_first=not player_stand and not game_over)
    draw_hand(player_hand, player_x, HEIGHT//2 + 60)
    dealer_val = hand_value(dealer_hand if player_stand or game_over else dealer_hand[1:])
    player_val = hand_value(player_hand)

    # Draw values
    if player_stand or game_over:
        dealer_val_text = font.render(f"Dealer: {hand_value(dealer_hand)}", True, (255,255,255))
    else:
        dealer_val_text = font.render("Dealer: ?", True, (255,255,255))
    player_val_text = font.render(f"Player: {player_val}", True, (255,255,255))
    screen.blit(dealer_val_text, (WIDTH//2 - dealer_val_text.get_width()//2, HEIGHT//2 - 190))
    screen.blit(player_val_text, (WIDTH//2 - player_val_text.get_width()//2, HEIGHT//2 + 40))

    # Show money and bet
    money_text = font.render(f"Money: ${player_money}", True, (255,255,0))
    bet_text = font.render(f"Bet: ${current_bet}", True, (255,255,0))
    screen.blit(money_text, (WIDTH - money_text.get_width() - 20, 20))
    screen.blit(bet_text, (WIDTH - bet_text.get_width() - 20, 60))

    # Instructions
    if not game_over:
        inst = font.render("Press H to Hit, S to Stand, R to Restart, Q to Quit", True, (255,255,255))
        screen.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT - 40))

    # Game logic
    if not game_over:
        if player_val > 21:
            result = "Bust! Dealer Wins."
            player_money -= current_bet
            game_over = True
        elif player_stand:
            # Dealer's turn
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            dealer_val = hand_value(dealer_hand)
            if dealer_val > 21 or player_val > dealer_val:
                result = "You Win!"
                player_money += current_bet
            elif player_val < dealer_val:
                result = "Dealer Wins."
                player_money -= current_bet
            else:
                result = "Push!"
            game_over = True

    if game_over:
        show_message(result, (255,255,0))
        again = font.render("Press R to play again or Q to quit.", True, (255,255,255))
        screen.blit(again, (WIDTH//2 - again.get_width()//2, HEIGHT//2 + 60))
        if player_money <= 0:
            broke = big_font.render("You're out of money!", True, (255,0,0))
            screen.blit(broke, (WIDTH//2 - broke.get_width()//2, HEIGHT//2 + 120))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit(); sys.exit()
            if not game_over:
                if event.key == pygame.K_h:
                    player_hand.append(deck.pop())
                elif event.key == pygame.K_s:
                    player_stand = True
            if event.key == pygame.K_r:
                if player_money > 0:
                    betting = True
                else:
                    player_money = 1000
                    betting = True

    pygame.display.flip()
    clock.tick(60)