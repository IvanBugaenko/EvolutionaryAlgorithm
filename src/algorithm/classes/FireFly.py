from __future__ import annotations
import numpy as np
import random


class FireFly:
    def __init__(self, N: int) -> None:
        """
        N: число городов (число вершин в графе)
        """
        self.N = N
        self.genotype = np.array([
            np.random.randint(0, N - i) for i in range(N)
        ])

    def __repr__(self) -> str:
        return f'{self.genotype}'

    def __len__(self) -> int:
        return self.N

    def __eq__(self, other: FireFly) -> bool:
        return np.all(self.genotype == other.genotype)

    def crossing(self, brighter_firefly: FireFly) -> None:
        """
        Оператор скрещивания (скрещивание будет модифицировать одну особь, которая имеет меньшую яркость)
        """
        divider = random.randint(1, self.N - 1)
        self.genotype[divider:] = brighter_firefly.genotype[divider:]

    def mutation(self) -> None:
        """
        [5, 4, 3, 2, 1, 0] - I
        ----------------------------------------
        [4, 0, 2, 1, 1, 0] - особь p

        [1, 4, 1, 1, 0, 0] - верхняя граница, сколько можно прибавить
        [4, 0, 2, 1, 1, 0] - верхняя граница, сколько можно отнять
        ----------------------------------------
        [5, 4, 3, 2, 1, 0] - особь p

        [0, 0, 0, 0, 0, 0] - верхняя граница, сколько можно прибавить
        [5, 4, 3, 2, 1, 0] - верхняя граница, сколько можно отнять
        ----------------------------------------
        [0, 0, 0, 0, 0, 0] - особь p

        [5, 4, 3, 2, 1, 0] - верхняя граница, сколько можно прибавить
        [0, 0, 0, 0, 0, 0] - верхняя граница, сколько можно отнять
        ----------------------------------------
        [-p, I - p] - границы
        """
        k = random.randint(0, self.N - 1)
        left_bound = -self.genotype[k]
        right_bound = self.N - 1 - k - self.genotype[k]
        self.genotype[k] += random.randint(left_bound, right_bound)

    def get_route(self) -> list[int]:
        L = list(range(self.N))
        return [L.pop(gene) for gene in self.genotype]
