import os
import pygame


class Tile:
    def __init__(self, value, image_name):
        self.val = value
        self.image_name = image_name


TILES_DICT = {
    "empty": Tile(0, "white.png"),
    "water": Tile(1, "water.png"),
    "farm": Tile(2, "farm.png"),
    "village": Tile(3, "village.png"),
    "forest": Tile(4, "forest.png"),
    "monster": Tile(5, "monster.png"),
    "mountain": Tile(6, "mountain.png"),
}


class Board:
    # Constants for the board size
    NR_OF_TILES = 11
    TILE_SIZE = 40  # Size of the square tile
    BOARD_SIZE = NR_OF_TILES * TILE_SIZE
    CARD_SIZE = (200, 300)
    SPACING = 10

    BOARD_LOCATION = (SPACING, CARD_SIZE[1] + SPACING * 2)
    EXPLORE_CARD_LOCATION = (
        SPACING * 2 + BOARD_SIZE,
        SPACING * 2 + CARD_SIZE[1],
    )
    WINDOW_SIZE = (
        CARD_SIZE[0] * 4 + SPACING * 5,
        TILE_SIZE * NR_OF_TILES + CARD_SIZE[1] + SPACING * 3,
    )


# Create the window
def init_screen():

    screen = pygame.display.set_mode(Board.WINDOW_SIZE)
    pygame.display.set_caption("Land Board")
    screen.fill((255, 255, 255))

    return screen


def load_scoring_card(name, alpha=False):
    path = os.path.join("images", "scoring_cards", name)
    image = pygame.transform.scale(pygame.image.load(path), Board.CARD_SIZE)
    if alpha:
        image.set_alpha(128)  # Set semi-transparent
    return image


def init_scoring_card_images(edicts):
    for _, scoring_card in edicts.items():
        scoring_card.img = load_scoring_card(scoring_card.image_path)
        scoring_card.img_prev = load_scoring_card(scoring_card.image_path, alpha=True)

    return edicts


def load_explore_card(name):
    path = os.path.join("images", "explore_cards", name)
    image = pygame.transform.scale(pygame.image.load(path), Board.CARD_SIZE)

    return image


def init_explore_card_images(cards):
    for card in cards:
        card.img = load_explore_card(card.image_path)

    return cards


# Load tile images
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


# Function to draw the preview based on relative positions
def draw_preview(screen, preview_pos, shape_positions, selected_tile_type):
    if preview_pos:
        for rel_pos in shape_positions:
            preview_col, preview_row = (
                preview_pos[0] + rel_pos[0],
                preview_pos[1] + rel_pos[1],
            )
            if (
                0 <= preview_col < Board.NR_OF_TILES
                and 0 <= preview_row < Board.NR_OF_TILES
            ):
                preview_tile = (
                    preview_col * Board.TILE_SIZE + Board.BOARD_LOCATION[0],
                    preview_row * Board.TILE_SIZE + Board.BOARD_LOCATION[1],
                )
                screen.blit(TILES[selected_tile_type].img_prev, preview_tile)


def tiles_overlap(board, pos, shape_positions):
    for rel_pos in shape_positions:
        col, row = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        if 0 <= col < Board.NR_OF_TILES and 0 <= row < Board.NR_OF_TILES:
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
        or max_x_offset >= Board.NR_OF_TILES
        or max_y_offset >= Board.NR_OF_TILES
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


def init_normal_board():
    board = [[0 for _ in range(Board.NR_OF_TILES)] for _ in range(Board.NR_OF_TILES)]
    mountains = [(3, 1), (8, 2), (5, 5), (2, 8), (7, 10)]
    for mountain in mountains:
        board[mountain[0]][mountain[1]] = 6
    return board


class GameState:
    def __init__(self, selected_shape, selected_tile_type, edicts):
        self.board = init_normal_board()
        self.screen = init_screen()
        self.hover_pos = (Board.NR_OF_TILES // 2, Board.NR_OF_TILES // 2)
        self.selected_shape = selected_shape
        self.selected_tile_type = selected_tile_type
        self.edicts = edicts
        self.running = True
        self.drawn = False

    def new_shape(self, selected_shape, selected_tile_type):
        self.hover_pos = (Board.NR_OF_TILES // 2, Board.NR_OF_TILES // 2)
        self.selected_shape = selected_shape
        self.selected_tile_type = selected_tile_type

    def update_edicts(self, active_edicts):
        self.screen.fill((255, 255, 255))

        edicts = ["A", "B", "C", "D"]
        for i, key in enumerate(edicts):
            image = (
                self.edicts[key].img
                if key in active_edicts
                else self.edicts[key].img_prev
            )
            position = (Board.SPACING * (i + 1) + Board.CARD_SIZE[0] * i, Board.SPACING)
            self.screen.blit(image, position)

    def update_explore_card(self, explore_card):
        print("update explore card")
        self.explore_card = explore_card
        self.explore_card_type_pointer = 0
        self.explore_card_shape_pointer = 0
        self.new_shape(explore_card.shapes[0], TILES_DICT[explore_card.types[0]].val)
        self.screen.blit(explore_card.img, Board.EXPLORE_CARD_LOCATION)

    def _explore_card_switch(self):
        if len(self.explore_card.types) > 1:
            self.explore_card_type_pointer += 1
            if self.explore_card_type_pointer == len(self.explore_card.types):
                self.explore_card_type_pointer = 0

            self.selected_tile_type = TILES_DICT[
                self.explore_card.types[self.explore_card_type_pointer]
            ].val
        elif len(self.explore_card.shapes) > 1:
            self.explore_card_shape_pointer += 1
            if self.explore_card_shape_pointer == len(self.explore_card.shapes):
                self.explore_card_shape_pointer = 0

            self.selected_shape = TILES_DICT[
                self.explore_card.shapes[self.explore_card_type_pointer]
            ].val

    # Function to draw/update the current board
    def _update_board(self):
        for col in range(Board.NR_OF_TILES):
            for row in range(Board.NR_OF_TILES):
                tile = (
                    col * Board.TILE_SIZE + Board.BOARD_LOCATION[0],
                    row * Board.TILE_SIZE + Board.BOARD_LOCATION[1],
                )
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
                elif event.key == pygame.K_t:
                    self._explore_card_switch()

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

        # self.screen.fill((255, 255, 255))  # Clear the screen to prevent artifacts
        self._update_board()
        draw_preview(
            self.screen, self.hover_pos, self.selected_shape, self.selected_tile_type
        )
        pygame.display.flip()
