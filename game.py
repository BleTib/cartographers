import pygame
from board import GameState, init_scoring_card_images, init_explore_card_images
from cards import SCORING_CARDS, EXPLORE_CARDS
import random

SHAPES = {
    "3x1": [(0, -1), (0, 0), (0, 1)],
    "Edge": [(0, 1), (0, 0), (1, 0)],
    "L": [(-1, 0), (0, 0), (1, 0), (1, 1)],
    # "T": [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)],
    "t": [(0, -1), (0, 0), (0, 1), (1, 0)],
}


class Season:
    def __init__(self, key, time, edicts):
        self.name = key
        self.time = time
        self.edicts = edicts


SEASONS = [
    Season("Spring", 8, ["A", "B"]),
    Season("Summer", 8, ["B", "C"]),
    Season("Fall", 7, ["C", "D"]),
    Season("Winter", 6, ["D", "A"]),
]


def new_shape():
    selected_shape = SHAPES[random.choice(list(SHAPES.keys()))]
    selected_tile_type = random.randint(1, 4)
    return selected_shape, selected_tile_type


def init_scoring_cards():
    scoring_cards = []
    for _, stack in SCORING_CARDS.items():
        scoring_cards.append(random.choice(stack))
    random.shuffle(scoring_cards)
    edicts = ["A", "B", "C", "D"]
    edicts = {edict: scoring_card for edict, scoring_card in zip(edicts, scoring_cards)}
    init_scoring_card_images(edicts)

    return edicts


def init_explore_cards():
    explore_cards = EXPLORE_CARDS.copy()
    random.shuffle(explore_cards)
    init_explore_card_images(explore_cards)

    return explore_cards


# explore phase
# draw a exploration card
# if ruin is drawn draw another one
# draw phase
# check phase


pygame.init()

edicts = init_scoring_cards()

# Main loop
selected_shape, selected_tile_type = new_shape()
gamestate = GameState(selected_shape, selected_tile_type, edicts)
score = 0
for season in SEASONS:
    if not gamestate.running:
        break
    gamestate.set_season(season)
    explore_cards = init_explore_cards()
    print()
    print("Season:", season.name)
    print("Time:", season.time)
    print(
        "Edicts:",
        season.edicts[0] + " - " + edicts[season.edicts[0]].name + " | ",
        season.edicts[1] + " - " + edicts[season.edicts[1]].name,
    )
    print()

    # Season rounds
    gamestate.timecost = 0
    gamestate.drawn = True  # that if clause can be accessed
    while gamestate.timecost < season.time and gamestate.running:
        if gamestate.drawn:
            explore_card = explore_cards.pop()
            gamestate.update_explore_card(explore_card)
            gamestate.draw_manager.update_board_screen()
        gamestate.draw_board()

    score1 = edicts[season.edicts[0]].score(gamestate.board)
    score2 = edicts[season.edicts[1]].score(gamestate.board)
    score += score1 + score2 + gamestate.coins
    print(
        "Score {}: {}".format(
            season.edicts[0] + " - " + edicts[season.edicts[0]].name, score1
        )
    )
    print(
        "Score {}: {}".format(
            season.edicts[1] + " - " + edicts[season.edicts[1]].name, score2
        )
    )
    print("Coins:", gamestate.coins)
    print("Total Score:", score)

# Wait until Quit Pygame
while gamestate.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamestate.running = False

pygame.quit()
