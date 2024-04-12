import os
import pygame
import random

from cards import TILES_DICT

# Initialize Pygame
pygame.init()

# Constants for the board size
BOARD_SIZE = 11
TILE_SIZE = 32  # Size of the square tile
WINDOW_SIZE = (TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE)


# Load images
def load_tile(name, alpha=False):
    path = os.path.join("images/tiles/basic", name)
    image = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))
    if alpha:
        image.set_alpha(128)  # Set semi-transparent
    return image


def init_tiles(tiles_dict):
    tiles = {}
    for _, tile in tiles_dict.items():
        tile.img = load_tile(tile.image_name)
        tile.img_prev = load_tile(tile.image_name, alpha=True)
        tiles[tile.val] = tile
    return tiles


TILES = init_tiles(TILES_DICT)

# Define shapes as lists of relative positions
SHAPES = {
    "3x1": [(0, -1), (0, 0), (0, 1)],
    "Edge": [(0, 1), (0, 0), (1, 0)],
    "L": [(-1, 0), (0, 0), (1, 0), (1, 1)],
    "T": [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)],
    "t": [(0, -1), (0, 0), (0, 1), (1, 0)],
}


# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Land Board")

# Create board
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


# Function to draw the board
def draw_board(screen):
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            tile = (col * TILE_SIZE, row * TILE_SIZE)
            type = board[col][row]
            screen.blit(TILES[type].img, tile)


# Function to draw the preview based on relative positions
def draw_preview(screen, preview_pos, shape_positions, selected_tile_type):
    if preview_pos:
        for rel_pos in shape_positions:
            preview_col, preview_row = (
                preview_pos[0] + rel_pos[0],
                preview_pos[1] + rel_pos[1],
            )
            if 0 <= preview_col < BOARD_SIZE and 0 <= preview_row < BOARD_SIZE:
                preview_tile = (preview_col * TILE_SIZE, preview_row * TILE_SIZE)
                screen.blit(TILES[selected_tile_type].img_prev, preview_tile)


def tiles_overlap(board, pos, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
            # Check if a tile already exists at this position
            if board[col][row] != 0:
                return True
    return False


# Function to place a tile on the board with relative positions
def place_tiles(board, pos, tile_type, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        board[col][row] = tile_type


# hover position not going out of bounds
def shape_out_of_bound(hover_pos, shape):
    min_x_offset = min(rel_pos[0] + hover_pos[0] for rel_pos in shape)
    min_y_offset = min(rel_pos[1] + hover_pos[1] for rel_pos in shape)
    max_x_offset = max(rel_pos[0] + hover_pos[0] for rel_pos in shape)
    max_y_offset = max(rel_pos[1] + hover_pos[1] for rel_pos in shape)
    if (
        min_x_offset < 0
        or min_y_offset < 0
        or max_x_offset >= BOARD_SIZE
        or max_y_offset >= BOARD_SIZE
    ):
        return True
    return False


# Rotate the shape 90 degrees
def rotate_shape(hover_pos, shape_positions, clockwise=True):
    if clockwise:
        new_positions = [(-pos[1], pos[0]) for pos in shape_positions]
    else:
        new_positions = [(pos[1], -pos[0]) for pos in shape_positions]

    if shape_out_of_bound(hover_pos, new_positions):
        return shape_positions
    return new_positions


# Flip the shape horizontally
def flip_shape(hover_pos, shape_positions):
    new_positions = [(-pos[0], pos[1]) for pos in shape_positions]
    if shape_out_of_bound(hover_pos, new_positions):
        return shape_positions
    return new_positions


def move_shape(hover_pos, new_pos_relative, selected_shape):
    new_pos = (hover_pos[0] + new_pos_relative[0], hover_pos[1] + new_pos_relative[1])
    if not shape_out_of_bound(new_pos, selected_shape):
        return new_pos
    return hover_pos


def new_shape():
    hover_pos = (BOARD_SIZE // 2, BOARD_SIZE // 2)
    selected_shape = SHAPES[random.choice(list(SHAPES.keys()))]
    selected_tile_type = random.randint(1, len(TILES) - 1)
    return hover_pos, selected_shape, selected_tile_type


# Initialize hover position and selected shape
hover_pos, selected_shape, selected_tile_type = new_shape()

# Main loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                selected_shape = rotate_shape(hover_pos, selected_shape)
            if event.key == pygame.K_q:
                selected_shape = rotate_shape(hover_pos, selected_shape, False)
            elif event.key == pygame.K_f:
                selected_shape = flip_shape(hover_pos, selected_shape)
            elif event.key == pygame.K_e:
                if not tiles_overlap(board, hover_pos, selected_shape):
                    place_tiles(board, hover_pos, selected_tile_type, selected_shape)
                    hover_pos, selected_shape, selected_tile_type = new_shape()
            # WASD keys to move the hover position
            elif event.key == pygame.K_w:
                hover_pos = move_shape(hover_pos, (0, -1), selected_shape)
            elif event.key == pygame.K_s:
                hover_pos = move_shape(hover_pos, (0, 1), selected_shape)
            elif event.key == pygame.K_a:
                hover_pos = move_shape(hover_pos, (-1, 0), selected_shape)
            elif event.key == pygame.K_d:
                hover_pos = move_shape(hover_pos, (1, 0), selected_shape)

    screen.fill((255, 255, 255))  # Clear the screen to prevent artifacts

    draw_board(screen)
    draw_preview(screen, hover_pos, selected_shape, selected_tile_type)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
