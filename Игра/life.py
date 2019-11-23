# coding=utf-8
import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        if randomize:
            A = []
            for i in range(self.rows):
                A.append([])
                for j in range(self.cols):
                    A[i].append(random.randint(0, 1))
            return A
        else:
            A = []
            for i in range(self.rows):
                A.append([])
                for j in range(self.cols):
                    A[i].append(0)
            return A


    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= cell[0] + i < self.rows and 0 <= cell[1] + j < self.cols and (i, j) != (0, 0):
                    neighbours.append(self.curr_generation[cell[0] + i][cell[1] + j])
        
        return neighbours


    def get_next_generation(self) -> Grid:
        A = []
        for i in range(self.rows):
            A.append([])
            for j in range(self.cols):
                N = self.get_neighbours((i, j))
                count = 0
                for value in N:
                    if value == 1:
                        count += 1

                val = self.prev_generation[i][j]
                if val == 1:
                    if count < 2:
                        A[i].append(0)
                    elif count < 4:
                        A[i].append(1)
                    else:
                        A[i].append(0)
                if val == 0:
                    if count == 3:
                        A[i].append(1)
                    else:
                        A[i].append(0)
        return A


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for i in range (self.rows):
            for j in range (self.cols):
                if self.curr_generation[i][j] != self.prev_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as f:
            L = list(f)
            A = []
            for i in range(len(L)):
                row = []
                for char in L[i]:
                    if char != '\n':
                        row.append(int(char))
                    else:
                        break
                A.append(row)
        rows = len(A)
        cols = len(A[0])
        size = (rows, cols)
        game = GameOfLife(size)
        game.curr_generation = A
        f.close()
        return game




    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for i in range(self.rows):
                for j in range(self.cols):
                    f.write(str(self.curr_generation[i][j]))
                f.write('\n')
        f.close()

