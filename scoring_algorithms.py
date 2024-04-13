import numpy as np
from board import TILES_DICT


def _dfs(i, j, cluster, visited):
    # traverse the board using dfs and return clusters of non visited cells
    if i < 0 or i >= len(visited) or j < 0 or j >= len(visited[0]) or visited[i][j]:
        return
    cluster.append((i, j))
    visited[i][j] = True
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        _dfs(i + dx, j + dy, cluster, visited)


def score_borderlands(board):
    arr = np.array(board)
    full_lines = np.count_nonzero(
        np.count_nonzero(arr, axis=1) == arr.shape[1]
    ) + np.count_nonzero(np.count_nonzero(arr, axis=0) == arr.shape[0])
    return full_lines * 6


def score_wildholds(board):

    visited = np.array(board) != TILES_DICT["village"].val
    clusters = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if not visited[i][j]:
                cluster = []
                _dfs(i, j, cluster, visited)
                if cluster:
                    clusters.append(cluster)

    # 8 points for each cluster of 6 or more villages
    return sum(8 for cluster in clusters if len(cluster) >= 6)


def score_canallake(board):
    def check_neighbours(board, x, y, value):
        potential_neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        # Filter out the neighbours that are out of bounds
        valid_neighbours = [
            (x, y)
            for x, y in potential_neighbours
            if 0 <= x < len(board) and 0 <= y < len(board[0])
        ]
        # Check the valid neighbours
        for x, y in valid_neighbours:
            if board[x][y] == value:
                return True
        return False

    scoring_board = np.zeros((len(board), len(board[0])), dtype=int)
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == TILES_DICT["water"].val and check_neighbours(
                board, x, y, TILES_DICT["farm"].val
            ):
                scoring_board[x][y] = 1
            elif board[x][y] == TILES_DICT["farm"].val and check_neighbours(
                board, x, y, TILES_DICT["water"].val
            ):
                scoring_board[x][y] = 1

    return sum(sum(scoring_board))


def score_sentinelwood(board):
    rows, cols = len(board), len(board[0])
    forest_tile = TILES_DICT["forest"].val
    score = 0

    # Traverse top and bottom edge
    for j in range(cols):
        if board[0][j] == forest_tile:
            score += 1
        if board[rows - 1][j] == forest_tile:
            score += 1

    # Traverse the left and right edge and skip corners as they are already covered
    for i in range(1, rows - 1):
        if board[i][0] == forest_tile:
            score += 1
        if board[i][cols - 1] == forest_tile:
            score += 1

    return score
