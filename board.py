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


class Window:
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
    FONT_SIZE = 36


# Create the window
def init_screen():
    screen = pygame.display.set_mode(Window.WINDOW_SIZE)
    pygame.display.set_caption("Land Board")
    screen.fill((255, 255, 255))

    return screen


def load_scoring_card(name, alpha=False):
    path = os.path.join("images", "scoring_cards", name)
    image = pygame.transform.scale(pygame.image.load(path), Window.CARD_SIZE)
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
    image = pygame.transform.scale(pygame.image.load(path), Window.CARD_SIZE)

    return image


def init_explore_card_images(cards):
    for card in cards:
        card.img = load_explore_card(card.image_path)

    return cards


# Load tile images
def load_tile(name, alpha=False):
    path = os.path.join("images", "tiles", "basic", name)
    image = pygame.transform.scale(
        pygame.image.load(path), (Window.TILE_SIZE, Window.TILE_SIZE)
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

MOUNTAINS = [(3, 1), (8, 2), (5, 5), (2, 8), (7, 9)]


def init_normal_board():
    board = [[0 for _ in range(Window.NR_OF_TILES)] for _ in range(Window.NR_OF_TILES)]
    for mountain in MOUNTAINS:
        board[mountain[0]][mountain[1]] = 6
    return board


class DrawManager:
    def __init__(self, game_state):
        self.gs = game_state

    def _shape_out_of_bound(self, hover_pos, shape):
        """Hover position not going out of bounds"""
        min_x_offset = min(rel_pos[0] + hover_pos[0] for rel_pos in shape)
        min_y_offset = min(rel_pos[1] + hover_pos[1] for rel_pos in shape)
        max_x_offset = max(rel_pos[0] + hover_pos[0] for rel_pos in shape)
        max_y_offset = max(rel_pos[1] + hover_pos[1] for rel_pos in shape)
        if (
            min_x_offset < 0
            or min_y_offset < 0
            or max_x_offset >= Window.NR_OF_TILES
            or max_y_offset >= Window.NR_OF_TILES
        ):
            return True
        return False

    def tiles_overlap(self):
        for rel_pos in self.gs.selected_shape:
            col, row = (
                self.gs.hover_pos[0] + rel_pos[0],
                self.gs.hover_pos[1] + rel_pos[1],
            )
            if 0 <= col < Window.NR_OF_TILES and 0 <= row < Window.NR_OF_TILES:
                # Check if a tile already exists at this position
                if self.gs.board[col][row] != 0:
                    return True
        return False

    def explore_card_switch(self):
        """Switch between the different types or shapes of the explore card."""
        if len(self.gs.explore_card.types) > 1:
            self.gs.explore_card_type_pointer += 1
            if self.gs.explore_card_type_pointer == len(self.gs.explore_card.types):
                self.gs.explore_card_type_pointer = 0

            self.gs.selected_tile_type = TILES_DICT[
                self.gs.explore_card.types[self.gs.explore_card_type_pointer]
            ].val

        elif len(self.gs.explore_card.shapes) > 1:
            self.gs.explore_card_shape_pointer = 1 - self.gs.explore_card_shape_pointer

            new_shape = self.gs.explore_card.shapes[self.gs.explore_card_shape_pointer]

            if self._shape_out_of_bound(self.gs.hover_pos, new_shape):
                self.gs.explore_card_shape_pointer = (
                    1 - self.gs.explore_card_shape_pointer
                )
            else:
                self.gs.selected_shape = new_shape

    def show_season(self):
        font = pygame.font.Font(None, Window.FONT_SIZE)
        text_surface = font.render(
            f"{self.gs.season.name}",
            True,
            (0, 0, 0),
            (255, 255, 255),
        )
        text_location = (
            Window.BOARD_SIZE + Window.SPACING * 2,
            Window.CARD_SIZE[1] * 2 + Window.SPACING * 3,
        )
        fill_rect = (
            text_location[0],
            text_location[1],
            Window.CARD_SIZE[0],
            Window.FONT_SIZE,
        )
        self.gs.screen.fill((255, 255, 255), fill_rect)
        self.gs.screen.blit(text_surface, text_location)

    def show_remaining_time(self):
        font = pygame.font.Font(None, Window.FONT_SIZE)
        time_left = max(
            0, self.gs.season.time - self.gs.timecost - self.gs.explore_card.timecost
        )
        text_surface = font.render(
            f"Time left: {time_left}",
            True,
            (0, 0, 0),
            (255, 255, 255),
        )
        self.gs.screen.blit(
            text_surface,
            (
                Window.BOARD_SIZE + Window.SPACING * 2,
                Window.CARD_SIZE[1] * 2 + Window.SPACING * 3 + Window.FONT_SIZE,
            ),
        )

    def show_coins(self):
        font = pygame.font.Font(None, Window.FONT_SIZE)
        text_surface = font.render(
            f"Coins: {self.gs.coins}",
            True,
            (0, 0, 0),
            (255, 255, 255),
        )
        self.gs.screen.blit(
            text_surface,
            (
                Window.BOARD_SIZE + Window.SPACING * 2,
                Window.CARD_SIZE[1] * 2 + Window.SPACING * 3 + Window.FONT_SIZE * 2,
            ),
        )

    def rotate_shape(self, clockwise=True):
        if clockwise:
            new_positions = [(-pos[1], pos[0]) for pos in self.gs.selected_shape]
        else:
            new_positions = [(pos[1], -pos[0]) for pos in self.gs.selected_shape]

        if self._shape_out_of_bound(self.gs.hover_pos, new_positions):
            return self.gs.selected_shape
        return new_positions

    def flip_shape(self):
        new_positions = [(-pos[0], pos[1]) for pos in self.gs.selected_shape]
        if self._shape_out_of_bound(self.gs.hover_pos, new_positions):
            return self.gs.selected_shape
        return new_positions

    def move_shape(self, new_pos_relative):
        new_hover_pos = (
            self.gs.hover_pos[0] + new_pos_relative[0],
            self.gs.hover_pos[1] + new_pos_relative[1],
        )
        if not self._shape_out_of_bound(new_hover_pos, self.gs.selected_shape):
            return new_hover_pos
        return self.gs.hover_pos

    def place_tiles(self):
        for rel_pos in self.gs.selected_shape:
            col, row = (
                self.gs.hover_pos[0] + rel_pos[0],
                self.gs.hover_pos[1] + rel_pos[1],
            )
            self.gs.board[col][row] = self.gs.selected_tile_type

    def _draw_preview(self):
        for rel_pos in self.gs.selected_shape:
            preview_col, preview_row = (
                self.gs.hover_pos[0] + rel_pos[0],
                self.gs.hover_pos[1] + rel_pos[1],
            )
            if (
                0 <= preview_col < Window.NR_OF_TILES
                and 0 <= preview_row < Window.NR_OF_TILES
            ):
                preview_tile = (
                    preview_col * Window.TILE_SIZE + Window.BOARD_LOCATION[0],
                    preview_row * Window.TILE_SIZE + Window.BOARD_LOCATION[1],
                )
                self.gs.screen.blit(
                    TILES[self.gs.selected_tile_type].img_prev, preview_tile
                )

    # Function to draw/update the current board
    def _update_board(self):
        for col in range(Window.NR_OF_TILES):
            for row in range(Window.NR_OF_TILES):
                tile = (
                    col * Window.TILE_SIZE + Window.BOARD_LOCATION[0],
                    row * Window.TILE_SIZE + Window.BOARD_LOCATION[1],
                )
                type = self.gs.board[col][row]
                self.gs.screen.blit(TILES[type].img, tile)

    def update_board_screen(self):
        self._update_board()
        self._draw_preview()
        self.show_remaining_time()
        self.show_coins()
        pygame.display.flip()


class KeyManager:
    def __init__(self, game_state):
        self.gs = game_state
        self.dm = game_state.draw_manager
        self.key_handler = {
            pygame.K_q: self._handle_key_q,
            pygame.K_r: self._handle_key_r,
            pygame.K_f: self._handle_key_f,
            pygame.K_e: self._handle_key_e,
            pygame.K_t: self._handle_key_t,
            pygame.K_w: self.handle_key_w,
            pygame.K_a: self.handle_key_a,
            pygame.K_s: self.handle_key_s,
            pygame.K_d: self.handle_key_d,
        }

    def _handle_key_q(self):
        self.gs.selected_shape = self.dm.rotate_shape(False)

    def _handle_key_r(self):
        self.gs.selected_shape = self.dm.rotate_shape()

    def _handle_key_f(self):
        self.gs.selected_shape = self.dm.flip_shape()

    def _handle_key_e(self):
        if not self.dm.tiles_overlap():
            self.dm.place_tiles()
            self.gs.timecost += self.gs.explore_card.timecost
            self.gs.coins += self.gs.explore_card.coins[
                self.gs.explore_card_shape_pointer
            ]
            self.gs._check_mountain_coins()
            if self.gs.coins > 14:
                self.gs.coins = 14
            self.gs.drawn = True

    def _handle_key_t(self):
        self.dm.explore_card_switch()

    def handle_key_w(self):
        self.gs.hover_pos = self.dm.move_shape((0, -1))

    def handle_key_a(self):
        self.gs.hover_pos = self.dm.move_shape((-1, 0))

    def handle_key_s(self):
        self.gs.hover_pos = self.dm.move_shape((0, 1))

    def handle_key_d(self):
        self.gs.hover_pos = self.dm.move_shape((1, 0))


class GameState:
    def __init__(self):
        self.draw_manager = DrawManager(self)
        self.key_manager = KeyManager(self)
        self.board = init_normal_board()
        self.screen = init_screen()
        self.hover_pos = (Window.NR_OF_TILES // 2, Window.NR_OF_TILES // 2)
        self.selected_shape = None
        self.selected_tile_type = None
        self.mountain_coins = MOUNTAINS.copy()
        self.coins = 0
        self.edicts = None
        self.season = None
        self.timecost = 0
        self.running = True
        self.drawn = False

    def _update_edicts(self, active_edicts):
        # (x, y, width, height)
        rect = (0, 0, Window.WINDOW_SIZE[0], Window.CARD_SIZE[1] + Window.SPACING * 2)
        self.screen.fill((255, 255, 255), rect)

        edicts = ["A", "B", "C", "D"]
        for i, key in enumerate(edicts):
            image = (
                self.edicts[key].img
                if key in active_edicts
                else self.edicts[key].img_prev
            )
            position = (
                Window.SPACING * (i + 1) + Window.CARD_SIZE[0] * i,
                Window.SPACING,
            )
            self.screen.blit(image, position)

    def set_season(self, season):
        self.season = season
        self._update_edicts(season.edicts)
        self.draw_manager.show_season()

    def set_edicts(self, edicts):
        self.edicts = edicts

    def _new_shape(self, selected_shape, selected_tile_type):
        self.hover_pos = (Window.NR_OF_TILES // 2, Window.NR_OF_TILES // 2)
        self.selected_shape = selected_shape
        self.selected_tile_type = selected_tile_type

    def update_explore_card(self, explore_card):

        self.explore_card = explore_card
        self.explore_card_type_pointer = 0
        self.explore_card_shape_pointer = 0
        self._new_shape(explore_card.shapes[0], TILES_DICT[explore_card.types[0]].val)
        self.screen.blit(explore_card.img, Window.EXPLORE_CARD_LOCATION)

        self.draw_manager.show_remaining_time()
        self.draw_manager.show_coins()

    def _check_mountain_coins(self):
        for mountain in self.mountain_coins:
            mountain_circled = True
            for pos in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if self.board[pos[0] + mountain[0]][pos[1] + mountain[1]] == 0:
                    mountain_circled = False
            if mountain_circled:
                self.coins += 1
                self.mountain_coins.remove(mountain)

    def draw_board(self):
        self.running, self.drawn = True, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_manager.key_handler:
                    self.key_manager.key_handler[event.key]()
                    self.draw_manager.update_board_screen()
