import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPE_COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (128, 128, 128)]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Create the game window

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize grid
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Initialize clock
clock = pygame.time.Clock()

# Initialize game variables
current_shape = None
current_shape_x = 0
current_shape_y = 0
score = 0

# Functions
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, SHAPE_COLORS[grid[y][x]], pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def new_shape():
    shape = random.choice(SHAPES)
    return shape

def draw_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                pygame.draw.rect(screen, SHAPE_COLORS[shape[row][col]], pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def collision(x, y, shape):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                if y + row >= GRID_HEIGHT or x + col < 0 or x + col >= GRID_WIDTH or grid[y + row][x + col] != 0:
                    return True
    return False

def place_shape(x, y, shape):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                grid[y + row][x + col] = shape[row][col]

def clear_lines():
    global score
    lines_cleared = 0
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            grid.pop(row)
            grid.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    score += lines_cleared * 100



# Initialize game variables
current_shape = None
current_shape_x = 0
current_shape_y = 0
score = 0
lines_eliminated = 0
current_level = "Medium"
extended_game = False
player_mode = True

def draw_dialog_box(message):
    dialog_font = pygame.font.Font(None, 17)
    dialog_text = dialog_font.render(message, True, WHITE)
    dialog_rect = dialog_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, BLACK, (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2), 2)
    screen.blit(dialog_text, dialog_rect)
    pygame.display.flip()

def handle_dialog_box():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # User chose "Yes"
                elif event.key == pygame.K_n:
                    return False  # User chose "No"


# Game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not collision(current_shape_x - 1, current_shape_y, current_shape):
                    current_shape_x -= 1
            if event.key == pygame.K_RIGHT:
                if not collision(current_shape_x + 1, current_shape_y, current_shape):
                    current_shape_x += 1
            if event.key == pygame.K_DOWN:
                if not collision(current_shape_x, current_shape_y + 1, current_shape):
                    current_shape_y += 1
            if event.key == pygame.K_UP:
                rotated_shape = list(zip(*current_shape[::-1]))
                if not collision(current_shape_x, current_shape_y, rotated_shape):
                    current_shape = rotated_shape
            if event.key == pygame.K_ESCAPE:
                draw_dialog_box("Do you want to end the game? (Y/N)")
                user_choice = handle_dialog_box()
                if user_choice:
                    game_over = True
                else:
                    # Close the dialog box
                    screen.fill(BLACK)
                    pygame.display.flip()

    if current_shape is None:
        current_shape = new_shape()
        current_shape_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
        current_shape_y = 0

    if not collision(current_shape_x, current_shape_y + 1, current_shape):
        current_shape_y += 1
    else:
        place_shape(current_shape_x, current_shape_y, current_shape)
        clear_lines()
        current_shape = None

    screen.fill(BLACK)
    draw_grid()
    if current_shape is not None:
        draw_shape(current_shape, current_shape_x, current_shape_y)

    # Display game information
    info_font = pygame.font.Font(None, 24)
    info_text = [
        f"Group: Group Number:9",
        f"Score: {score}",
        f"Lines Eliminated: {lines_eliminated}",
        f"Level: {current_level}",
        f"Extended Game: {'Yes' if extended_game else 'No'}",
        f"Player Mode: {'Player' if player_mode else 'AI'}"
    ]
    y_position = 10
    for text in info_text:
        info_rendered = info_font.render(text, True, WHITE)
        info_rect = info_rendered.get_rect(topleft=(10, y_position))
        screen.blit(info_rendered, info_rect)
        y_position += 30

    pygame.display.flip()
    clock.tick(5)

# Clean up
pygame.quit()

sys.exit()
