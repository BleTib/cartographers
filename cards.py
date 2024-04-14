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
        "great_river.jpg",
        "Great River",
        1,
        ["water"],
        [[(0, -1), (0, 0), (0, 1)], [(0, 0), (0, 1), (-1, 1), (1, 0), (1, -1)]],
        [1, 0],
    ),
    ExploreCard(
        "farmland.jpg",
        "Farmland",
        1,
        ["farm"],
        [[(0, 0), (0, -1)], [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]],
        [1, 0],
    ),
    ExploreCard(
        "hamlet.jpg",
        "Hamlet",
        1,
        ["village"],
        [[(0, 0), (0, -1), (1, 0)], [(-1, 0), (0, 0), (-1, -1), (0, -1), (1, -1)]],
        [1, 0],
    ),
    ExploreCard(
        "forgotten_forest.jpg",
        "Forgotten Forest",
        1,
        ["forest"],
        [[(0, 0), (1, 1)], [(0, -1), (0, 0), (1, 0), (1, 1)]],
        [1, 0],
    ),
    ExploreCard(
        "hinterland_stream.jpg",
        "Hinterland Stream",
        2,
        ["farm", "water"],
        [[(0, 2), (0, 1), (0, 0), (1, 0), (2, 0)]],
        [0],
    ),
    ExploreCard(
        "orchard.jpg",
        "Orchard",
        2,
        ["forest", "farm"],
        [[(-1, 0), (0, 0), (1, 0), (1, 1)]],
        [0],
    ),
    ExploreCard(
        "treetop_village.jpg",
        "Treetop Village",
        2,
        ["forest", "village"],
        [[(-2, 0), (-1, 0), (0, 0), (0, -1), (1, -1)]],
        [0],
    ),
    ExploreCard(
        "fishing_village.jpg",
        "Fishing Village",
        2,
        ["village", "water"],
        [[(-2, 0), (-1, 0), (0, 0), (1, 0)]],
        [0],
    ),
    ExploreCard(
        "rift_lands.jpg",
        "Rift Lands",
        0,
        ["forest", "village", "farm", "water", "monster"],
        [[(0, 0)]],
        [0],
    ),
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
