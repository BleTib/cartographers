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
