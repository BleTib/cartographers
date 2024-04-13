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
    "forest": [
        ScoringCard(
            "sentinelwood.jpeg",
            "Sentinel Wood",
            scoring_algorithms.score_sentinelwood,
        )
    ],
    "village": [
        ScoringCard(
            "wildholds.jpeg",
            "Wildholds",
            scoring_algorithms.score_wildholds,
        )
    ],
    "land+water": [
        ScoringCard(
            "canallake.jpeg",
            "Canal Lake",
            scoring_algorithms.score_canallake,
        )
    ],
    "space": [
        ScoringCard(
            "borderlands.jpeg",
            "Borderlands",
            scoring_algorithms.score_borderlands,
        )
    ],
}
