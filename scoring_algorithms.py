import numpy as np


def score_borderlands(board):
    arr = np.array(board)
    return np.count_nonzero(
        np.count_nonzero(arr, axis=1) == arr.shape[1]
    ) + np.count_nonzero(np.count_nonzero(arr, axis=0) == arr.shape[0])
