import numpy as np


def generate_field(N: int, n_food: int) -> np.ndarray:
    ones = np.ones(n_food)
    zeros = np.zeros(N ** 2 - n_food)
    field = np.hstack((ones, zeros))
    np.random.shuffle(field)
    return field.reshape(N, N)
