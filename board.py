import os
import pygame

from cards import TILES_DICT

# Initialize Pygame
pygame.init()


class Board:
    # Constants for the board size
    BOARD_SIZE = 11
    TILE_SIZE = 32  # Size of the square tile
    WINDOW_SIZE = (TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE)


# Load images
def load_tile(name, alpha=False):
    path = os.path.join("images", "tiles", "basic", name)
    image = pygame.transform.scale(
        pygame.image.load(path), (Board.TILE_SIZE, Board.TILE_SIZE)
    )
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


# Create the window
def init_screen():
    screen = pygame.display.set_mode(Board.WINDOW_SIZE)
    pygame.display.set_caption("Land Board")
    return screen


# Function to draw the preview based on relative positions
def draw_preview(screen, preview_pos, shape_positions, selected_tile_type):
    if preview_pos:
        for rel_pos in shape_positions:
            preview_col, preview_row = (
                preview_pos[0] + rel_pos[0],
                preview_pos[1] + rel_pos[1],
            )
            if (
                0 <= preview_col < Board.BOARD_SIZE
                and 0 <= preview_row < Board.BOARD_SIZE
            ):
                preview_tile = (
                    preview_col * Board.TILE_SIZE,
                    preview_row * Board.TILE_SIZE,
                )
                screen.blit(TILES[selected_tile_type].img_prev, preview_tile)


def tiles_overlap(board, pos, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        if 0 <= col < Board.BOARD_SIZE and 0 <= row < Board.BOARD_SIZE:
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
        or max_x_offset >= Board.BOARD_SIZE
        or max_y_offset >= Board.BOARD_SIZE
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


class GameState:
    def __init__(self, screen, selected_shape, selected_tile_type):
        self.board = [
            [0 for _ in range(Board.BOARD_SIZE)] for _ in range(Board.BOARD_SIZE)
        ]
        self.screen = screen
        self.hover_pos = (Board.BOARD_SIZE // 2, Board.BOARD_SIZE // 2)
        self.selected_shape = selected_shape
        self.selected_tile_type = selected_tile_type
        self.running = True
        self.drawn = False

    def new_shape(self, selected_shape, selected_tile_type):
        self.hover_pos = (Board.BOARD_SIZE // 2, Board.BOARD_SIZE // 2)
        self.selected_shape = selected_shape
        self.selected_tile_type = selected_tile_type

    # Function to draw/update the current board
    def _update_board(self):
        for col in range(Board.BOARD_SIZE):
            for row in range(Board.BOARD_SIZE):
                tile = (col * Board.TILE_SIZE, row * Board.TILE_SIZE)
                type = self.board[col][row]
                self.screen.blit(TILES[type].img, tile)

    def draw_board(self):
        self.running, self.drawn = True, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.selected_shape = rotate_shape(
                        self.hover_pos, self.selected_shape
                    )
                if event.key == pygame.K_q:
                    self.selected_shape = rotate_shape(
                        self.hover_pos, self.selected_shape, False
                    )
                elif event.key == pygame.K_f:
                    self.selected_shape = flip_shape(
                        self.hover_pos, self.selected_shape
                    )
                elif event.key == pygame.K_e:
                    if not tiles_overlap(
                        self.board, self.hover_pos, self.selected_shape
                    ):
                        place_tiles(
                            self.board,
                            self.hover_pos,
                            self.selected_tile_type,
                            self.selected_shape,
                        )
                        self.drawn = True
                # WASD keys to move the hover position
                elif event.key == pygame.K_w:
                    self.hover_pos = move_shape(
                        self.hover_pos, (0, -1), self.selected_shape
                    )
                elif event.key == pygame.K_s:
                    self.hover_pos = move_shape(
                        self.hover_pos, (0, 1), self.selected_shape
                    )
                elif event.key == pygame.K_a:
                    self.hover_pos = move_shape(
                        self.hover_pos, (-1, 0), self.selected_shape
                    )
                elif event.key == pygame.K_d:
                    self.hover_pos = move_shape(
                        self.hover_pos, (1, 0), self.selected_shape
                    )

        self.screen.fill((255, 255, 255))  # Clear the screen to prevent artifacts
        self._update_board()
        draw_preview(
            self.screen, self.hover_pos, self.selected_shape, self.selected_tile_type
        )
        pygame.display.flip()
