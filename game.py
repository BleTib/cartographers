import pygame
from board import Board, TILES, GameState, init_screen
import random

SHAPES = {
    "3x1": [(0, -1), (0, 0), (0, 1)],
    "Edge": [(0, 1), (0, 0), (1, 0)],
    "L": [(-1, 0), (0, 0), (1, 0), (1, 1)],
    "T": [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)],
    "t": [(0, -1), (0, 0), (0, 1), (1, 0)],
}


def new_shape():
    selected_shape = SHAPES[random.choice(list(SHAPES.keys()))]
    selected_tile_type = random.randint(1, len(TILES) - 1)
    return selected_shape, selected_tile_type


# explore phase
# draw a exploration card
# if ruin is drawn draw another one
# draw phase
# check phase


# init board
# init edicts and scoring cards

# init season (both scoring cards

# start game
# for scorings in seasons:

pygame.init()
screen = init_screen()

season_time = 8
timecost = 0

# Main loop
selected_shape, selected_tile_type = new_shape()
gamestate = GameState(screen, selected_shape, selected_tile_type)

while timecost < season_time and gamestate.running:
    if gamestate.drawn:
        print("timecost", timecost)
        selected_shape, selected_tile_type = new_shape()
        gamestate.new_shape(selected_shape, selected_tile_type)
        timecost += 1
    gamestate.draw_board()

# Quit Pygame
pygame.quit()
