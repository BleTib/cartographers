import scoring_algorithms


class ExploreCard:
    def __init__(self, image_path, name, timecost, types, shapes, coins):
        self.image_path = image_path
        self.name = name
        self.timecost = timecost
        self.types = types
        self.shapes = shapes
        self.coins = coins


EXPLORE_CARDS = [
    ExploreCard(
        "images/explore_cards/fishing_village.jpg",
        "Fishing Village",
        2,
        ["village", "water"],
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        [0],
    )
]


class ScoringCard:
    def __init__(self, image_path, name, scoring_algorithm):
        self.image_path = image_path
        self.name = name
        self.scoring_algorithm = scoring_algorithm

    def score(self, board):
        return self.scoring_algorithm(board)


SCORING_CARDS = {
    "forest": [],
    "village": [],
    "land+water": [],
    "space": [
        ScoringCard(
            "images/scoring_cards/borderlands.jpeg",
            "Borderlands",
            scoring_algorithms.score_borderlands,
        )
    ],
}


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
