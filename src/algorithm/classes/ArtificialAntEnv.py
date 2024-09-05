import numpy as np


class ArtificialAntEnv:
    def __init__(
            self, 
            start_field: np.ndarray, 
            start_pos: tuple[int, int] = (0, 0), 
            start_angle: int = 0,
            max_food: int = 90):
        """
        field: 32 x 32, заполненное нулями, с едой.
        
        angle:
            - 0 - право;
            - 1 - низ;
            - 2 - лево;
            - 3 - верх.

        designations:
            - 0 - пустая ячейка;
            - 1 - в ячейке присутствует еда;
            - 2 - траектория муравья, если он прошел по пустой ячейке;
            - 3 - траектория муравья, если он прошел по ячейке с едой.
        """
        self.N = start_field.shape[0]

        self.start_field = start_field
        self.start_pos = start_pos
        self.start_angle = start_angle

        self.max_food = max_food
        
        self.field = None
        self.current_angle = None
        self.current_pos = None

    def reset(self) -> tuple[bool, bool]:
        """
        return: tuple[bool, bool]
            - t[0]: True, если была съедена еда на данном ходу
            - t[1]: True, если муравей видит еду перед собой
        """
        self.field = self.start_field.copy()
        self.current_angle = self.start_angle
        self.current_pos = self.start_pos

        self.field[self.current_pos] = 3 if self.field[self.current_pos] in [1, 3] else 2

        return self.field[self.current_pos] == 3, self.field[self.__get_new_pos()] == 1

    def __rotate(self, angle_value: int) -> None:
        self.current_angle = (self.current_angle + angle_value) % 4

    def __get_new_pos(self) -> tuple[int, int]:
        match self.current_angle:
            case 0: # пойти направо
                new_pos = (self.current_pos[0], (self.current_pos[1] + 1) % self.N)
            case 1: # пойти вниз
                new_pos = ((self.current_pos[0] - 1) % self.N, self.current_pos[1])
            case 2: # пойти налево
                new_pos = (self.current_pos[0], (self.current_pos[1] - 1) % self.N)
            case 3: # пойти вверх
                new_pos = ((self.current_pos[0] + 1) % self.N, self.current_pos[1])
        return new_pos

    def __forward(self) -> bool:
        new_pos = self.__get_new_pos()
        is_eat = self.field[new_pos] == 1
        self.field[new_pos] = 3 if self.field[new_pos] in [1, 3] else 2
        self.current_pos = new_pos

        return is_eat

    def step(self, action: int) -> tuple[bool, bool]:
        """
        actions:
            - 0 - идти прямо, вдоль текущего угла;
            - 1 - повернуть налево;
            - 2 - повернуть направо.

        return: tuple[bool, bool]
            - t[0]: True, если была съедена еда на данном ходу
            - t[1]: True, если муравей видит еду перед собой
        """
        is_eat = False
        match action:
            case 0:
                is_eat = self.__forward()
            case 1:
                self.__rotate(-1)
            case 2:
                self.__rotate(1)
        
        return is_eat, self.field[self.__get_new_pos()] == 1
