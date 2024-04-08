import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants for the board size
BOARD_SIZE = 11
TILE_SIZE = 32  # Size of the square tile
WINDOW_SIZE = (TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE)


# Load images
def load_image(name, alpha=False):
    path = os.path.join("images", name)
    image = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))
    if alpha:
        image.set_alpha(128)  # Set semi-transparent
    return image


# Images for tiles
tiles = {
    0: load_image("white.png"),
    1: load_image("tree.png"),
    2: load_image("water.png"),
}

# Semi-transparent tiles for preview
preview_tiles = {
    1: load_image("tree.png", alpha=True),
    2: load_image("water.png", alpha=True),
}

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Land Board")

# Create board
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Currently selected tile type (1 for tree, 2 for water, etc.)
selected_tile_type = 1


# Function to draw the board
def draw_board(screen):
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            tile = (col * TILE_SIZE, row * TILE_SIZE)
            field = board[col][row]
            screen.blit(tiles[field], tile)


# Function to draw the preview based on relative positions
def draw_preview(screen, preview_pos, shape_positions):
    if preview_pos:
        for rel_pos in shape_positions:
            preview_col, preview_row = (
                preview_pos[0] + rel_pos[0],
                preview_pos[1] + rel_pos[1],
            )
            if 0 <= preview_col < BOARD_SIZE and 0 <= preview_row < BOARD_SIZE:
                preview_tile = (preview_col * TILE_SIZE, preview_row * TILE_SIZE)
                screen.blit(preview_tiles[selected_tile_type], preview_tile)


def check_tiles(board, pos, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
            # Check if a tile already exists at this position
            if board[col][row] != 0:
                return False
    return True


# Function to place a tile on the board with relative positions
def place_tiles(board, pos, tile_type, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        board[col][row] = tile_type


# Define shapes as lists of relative positions
SHAPES = {
    "3x1": [(0, -1), (0, 0), (0, 1)],
    "Edge": [(0, 1), (0, 0), (1, 0)],
    "L": [(-1, 0), (0, 0), (1, 0), (1, 1)],
    "T": [(0, -1), (0, 0), (0, 1), (1, 0), (2, 0)],
    "t": [(0, -1), (0, 0), (0, 1), (1, 0)],
}


# Function to rotate the relative positions
def rotate_shape(shape_positions):
    # Swap x and y for each position to rotate 90 degrees
    return [(pos[1], pos[0]) for pos in shape_positions]


# Function to flip the relative positions
def flip_shape(shape_positions):
    # FLip the shape to mirror it
    return [(-pos[0], pos[1]) for pos in shape_positions]


# Adjust hover position based on the current shape
def adjust_hover_pos(hover_pos, shape):
    max_col_offset = max(rel_pos[0] for rel_pos in shape)
    max_row_offset = max(rel_pos[1] for rel_pos in shape)
    adjusted_col = min(hover_pos[0], BOARD_SIZE - 1 - max_col_offset)
    adjusted_row = min(hover_pos[1], BOARD_SIZE - 1 - max_row_offset)
    return adjusted_col, adjusted_row


def new_shape():
    hover_pos = (BOARD_SIZE // 2, BOARD_SIZE // 2)
    selected_shape = SHAPES[random.choice(list(SHAPES.keys()))]
    return hover_pos, selected_shape


hover_pos, selected_shape = new_shape()
# Main loop
running = True
while running:

    hover_pos = adjust_hover_pos(hover_pos, selected_shape)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                selected_shape = rotate_shape(selected_shape)
            elif event.key == pygame.K_f:
                selected_shape = flip_shape(selected_shape)
            elif event.key == pygame.K_e:
                if check_tiles(board, hover_pos, selected_shape):
                    place_tiles(board, hover_pos, selected_tile_type, selected_shape)
                    hover_pos, selected_shape = new_shape()
            # WASD keys to move the hover position
            elif event.key == pygame.K_w:
                hover_pos = (hover_pos[0], max(0, hover_pos[1] - 1))
            elif event.key == pygame.K_s:
                hover_pos = (hover_pos[0], min(BOARD_SIZE - 1, hover_pos[1] + 1))
            elif event.key == pygame.K_a:
                hover_pos = (max(0, hover_pos[0] - 1), hover_pos[1])
            elif event.key == pygame.K_d:
                hover_pos = (min(BOARD_SIZE - 1, hover_pos[0] + 1), hover_pos[1])

    screen.fill((0, 0, 0))  # Clear the screen with a black color
    draw_board(screen)
    draw_preview(screen, hover_pos, selected_shape)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
