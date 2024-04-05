from typing import Iterable
from .FireFly import FireFly
import numpy as np
import random


class Environment:
    def __init__(self, N: int, adjacency_matrix: np.ndarray, gamma: float = 0.9) -> None:
        """
        adjacency_matrix: матрица смежности (определяет длину пути из городов)
        gamma: уровень значимости привлекательности света для особей (
            если gamma -> 0, то светлячки со схожей яркостью не будут обращать друг на друга внимание, 
            если gamma -> 1, то светлячки со схожей яркостью будут всегда обращать друг на друга внимание
        )
        """
        self.N = N
        self.adjacency_matrix = adjacency_matrix
        self.gamma = gamma

    def __fitness(self, individual: FireFly) -> float:
        route = individual.get_route()
        return self.adjacency_matrix[route[-1], route[0]] + sum([
            self.adjacency_matrix[route[i], route[i + 1]] for i in range(len(route) - 1)
        ])

    def __init_population(self, population_size: int) -> Iterable[FireFly]:
        return [FireFly(self.N) for _ in range(population_size)]

    def __crossing_step(self, population: Iterable[FireFly], population_size: int, mutation_probability: float) -> None:
        for i in range(population_size):
            for j in range(population_size):
                if i < j:
                    p1: FireFly = population[i]
                    p2: FireFly = population[j]
                    p1_fitness = self.__fitness(p1)
                    p2_fitness = self.__fitness(p2)
                    pairs = [
                        (i, p1, p1_fitness), (j, p2, p2_fitness)
                    ]
                    min_fitness_firefly = min(pairs, key=lambda pair: pair[-1])
                    max_fitness_firefly = max(pairs, key=lambda pair: pair[-1])
                    if min_fitness_firefly[-1] / max_fitness_firefly[-1] < self.gamma:
                        population[max_fitness_firefly[0]].crossing(
                            min_fitness_firefly[1])
                    if random.random() < mutation_probability:
                        population[min_fitness_firefly[0]].mutation()

    def __find_best_individual(self, population: Iterable[FireFly]) -> tuple[float, list[int]]:
        sorted_population = sorted(
            population,
            key=lambda individual: self.__fitness(individual)
        )
        best_individual = sorted_population[0]
        return (
            self.__fitness(best_individual), best_individual.get_route()
        )

    def get_answer(self, population_size: int, mutation_probability: float = 0.1, k_max: int = 200) -> tuple[
        float, list[int], list[tuple[float, list[int]]]
    ]:
        """
        population_size: размер популяции светлячков
        mutation_probability: вероятность мутации лучшей особи
        k_max: ограничение по числу итераций алгоритма
        """
        population = self.__init_population(population_size)

        best_fitness, best_route = self.__find_best_individual(population)

        best_list: list[tuple[float, list[int]]] = [(best_fitness, best_route)]

        for _ in range(k_max):
            self.__crossing_step(
                population, population_size, mutation_probability)
            population_best_fitness, population_best_route = self.__find_best_individual(
                population)
            best_list.append((population_best_fitness, population_best_route))
            if population_best_fitness < best_fitness:
                best_fitness = population_best_fitness
                best_route = population_best_route

        return best_fitness, best_route, best_list
