from __future__ import annotations
import numpy as np
from .ArtificialAntEnv import ArtificialAntEnv


class FSM:
    def __init__(
            self, 
            n_state: int, 
            n_action: int, 
            start_field: np.ndarray,
            fsm: np.ndarray | None = None
        ) -> None:

        self.n_state = n_state
        self.n_action = n_action

        self.env = ArtificialAntEnv(start_field)

        self.fsm = np.hstack([
            np.random.randint(0, n_action, size=(n_state, 1)),
            np.random.randint(0, n_state, size=(n_state, 1)),
            np.random.randint(0, n_action, size=(n_state, 1)),
            np.random.randint(0, n_state, size=(n_state, 1)),
        ]) if fsm is None else fsm

        self.fitness = 0

    @staticmethod
    def crossing(fsm1: FSM, fsm2: FSM) -> tuple[FSM, FSM]:
        child1, child2 = fsm1.fsm.copy(), fsm2.fsm.copy()

        m, _ = child1.shape
        n_action = fsm1.n_action
        start_field = fsm1.env.start_field

        k = np.random.randint(1, m - 1)
        child1[k:, :], child2[k:, :] = child2[k:, :], child1[k:, :].copy()

        return (
            FSM(n_state=m, n_action=n_action, start_field=start_field, fsm=child1),
            FSM(n_state=m, n_action=n_action, start_field=start_field, fsm=child2)
        )
    
    def mutation(self) -> None:
        k = np.random.randint(0, self.n_state)
        self.fsm[k, :] = np.array([
            np.random.randint(0, self.n_action),
            np.random.randint(0, self.n_state),
            np.random.randint(0, self.n_action),
            np.random.randint(0, self.n_state),
        ])

    def __fsm_step(self, state: int, is_see_food: bool) -> tuple[int, int]:
        """
        return: tuple[int, int]
            - t[0]: действие
            - t[1]: следующее состояние
        """
        part = self.fsm[state, 2:] if is_see_food else self.fsm[state, :2]
        action, next_state = part
        return action, next_state

    def run_episode(self, k_max: int) -> int:
        state = 0
        is_eat, is_see_food = self.env.reset()
        i = 0
        total_reward = int(is_eat)
        while i != k_max and total_reward != self.env.max_food:
            action, state = self.__fsm_step(state, is_see_food)
            is_eat, is_see_food = self.env.step(action)
            i += 1
            total_reward += int(is_eat)

        self.fitness = total_reward
        return total_reward
