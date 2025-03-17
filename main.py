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

CANDY_COLORS = [DARK_RED, DARK_GREEN, DARK_BLUE, GOLD_YELLOW, DEEP_ORANGE, VIOLET, WHITE]

board = [[random.choice(CANDY_COLORS) for _ in range(COLS)] for _ in range(ROWS)]

selected_block = None

falling_blocks = []

def update_board():
    for col in range(COLS):
        empty_cells = 0
        for row in range(ROWS-1, -1, -1):
            if board[row][col] is None:
                empty_cells += 1
            elif empty_cells > 0:
                board[row + empty_cells][col] = board[row][col]
                board[row][col] = None
                falling_blocks.append({'color': board[row + empty_cells][col], 'row': row + empty_cells, 'col': col, 'y': row * BLOCK_SIZE, 'target_y': (row + empty_cells) * BLOCK_SIZE})
    for col in range(COLS):
        for row in range(ROWS):
            if board[row][col] is None:
                board[row][col] = random.choice(CANDY_COLORS)

def find_matches():
    matches = []
    for row in range(ROWS):
        for col in range(COLS - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] and board[row][col] is not None:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))
    for col in range(COLS):
        for row in range(ROWS - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] and board[row][col] is not None:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))
    return matches

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
                    if (row, col) not in find_matches() and (selected_row, selected_col) not in find_matches():
                        board[row][col], board[selected_row][selected_col] = board[selected_row][selected_col], board[row][col]
                    selected_block = None

    update_board()

    matches = find_matches()
    score = 0

    if matches:
      score += len(matches) * 10

    if matches:
        for row, col in matches:
            board[row][col] = None

    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):
            color = board[row][col]
            if color is not None:
                rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    if selected_block is not None:
        row, col = selected_block
        pygame.draw.rect(screen, (255, 255, 0), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 4)

    for block in falling_blocks:
        if block['y'] < block['target_y']:
            block['y'] += 0.5 
        else:
            falling_blocks.remove(block)
        pygame.draw.rect(screen, block['color'], (block['col'] * BLOCK_SIZE, block['y'], BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()

pygame.quit()