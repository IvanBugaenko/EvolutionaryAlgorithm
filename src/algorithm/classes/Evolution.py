import numpy as np
from .FSM import FSM
from typing import Iterable


class Evolution:
    def __init__(self, field: np.ndarray):
        self.field = field

    def __random_selection(self, population: list[FSM]) -> Iterable[tuple[FSM, FSM]]:
        n = len(population)

        first = population[:n//2]
        np.random.shuffle(first)

        second = population[n//2:]
        np.random.shuffle(second)

        return zip(first, second)

    def get_answer(
            self,
            n_state: int, 
            epoch: int, 
            population_size: int, 
            crossing_probability: float, 
            mutation_probability: float
        ) -> tuple[FSM, list[int]]:

        population = [
            FSM(n_state, 3, self.field) for _ in range(population_size)
        ]

        best_individuals: list[FSM] = []

        for _ in range(epoch):
            parents = self.__random_selection(population)

            for p1, p2 in parents:
                if np.random.rand() <= crossing_probability:
                    c1, c2 = FSM.crossing(p1, p2)
                    population.append(c1)
                    population.append(c2)

            for individual in population:
                if np.random.rand() <= mutation_probability:
                    individual.mutation()
                individual.run_episode(300)

            sorted_population = sorted(population, key=lambda x: x.fitness)
            best_individuals.append(sorted_population[-1])

            population = sorted_population[-population_size:]

        best_individual = sorted(best_individuals, key=lambda x: x.fitness)[-1]

        return best_individual, [
            individual.fitness for individual in best_individuals
        ]
