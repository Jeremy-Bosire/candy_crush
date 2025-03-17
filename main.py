import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 9, 9
BLOCK_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JEREMY'S CANDY CRUSH GAME")

DARK_RED = (200, 0, 0)
DARK_GREEN = (0, 200, 0)
DARK_BLUE = (0, 0, 200)
GOLD_YELLOW = (200, 200, 0)
DEEP_ORANGE = (255, 140, 0)
VIOLET = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CANDY_COLORS = [DARK_RED, DARK_GREEN, DARK_BLUE, GOLD_YELLOW, DEEP_ORANGE, VIOLET]

board = [[random.choice(CANDY_COLORS) for _ in range(COLS)] for _ in range(ROWS)]
selected_block = None
falling_blocks = []
score = 0
font = pygame.font.Font(None, 36)

def update_board():
    global board
    for col in range(COLS):
        empty_cells = 0
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] is None:
                empty_cells += 1
            elif empty_cells > 0:
                board[row + empty_cells][col] = board[row][col]
                board[row][col] = None
    for col in range(COLS):
        for row in range(ROWS):
            if board[row][col] is None:
                board[row][col] = random.choice(CANDY_COLORS)

def find_matches():
    matches = set()
    for row in range(ROWS):
        for col in range(COLS - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2]:
                matches.update([(row, col), (row, col + 1), (row, col + 2)])
    for col in range(COLS):
        for row in range(ROWS - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col]:
                matches.update([(row, col), (row + 1, col), (row + 2, col)])
    return list(matches)

def has_possible_moves():
    for row in range(ROWS):
        for col in range(COLS - 1):
            board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
            if find_matches():
                board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
                return True
            board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
    for col in range(COLS):
        for row in range(ROWS - 1):
            board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
            if find_matches():
                board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
                return True
            board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
    return False

def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = board[row][col]
            if color is not None:
                rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
    if selected_block is not None:
        row, col = selected_block
        pygame.draw.rect(screen, (255, 255, 0), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 4)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // BLOCK_SIZE
            row = mouse_y // BLOCK_SIZE
            if selected_block is None:
                selected_block = (row, col)
            else:
                selected_row, selected_col = selected_block
                if abs(row - selected_row) + abs(col - selected_col) == 1:
                    board[row][col], board[selected_row][selected_col] = board[selected_row][selected_col], board[row][col]
                    if not find_matches():
                        board[row][col], board[selected_row][selected_col] = board[selected_row][selected_col], board[row][col]
                    selected_block = None

    matches = find_matches()
    if matches:
        score += len(matches) * 10
        for row, col in matches:
            board[row][col] = None
        update_board()

    if not has_possible_moves():
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    draw_board()

pygame.quit()
