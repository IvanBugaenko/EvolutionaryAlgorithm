import numpy as np


def get_graph(file) -> np.ndarray:
    N = int(file[0].strip())
    matrix = np.zeros((N, N))
    for row in file[1:]:
        v1, v2, value = row.strip().split()
        matrix[int(v1) - 1, int(v2) - 1] = value
        matrix[int(v2) - 1, int(v1) - 1] = value
    return N, matrix
