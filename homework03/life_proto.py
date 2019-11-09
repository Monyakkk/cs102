# coding=utf-8
import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создаем поколения для начала игры
        self.grid = self.create_grid(randomize=True)
        self.previous_generation = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)
        self.previous_generation = self.create_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.previous_generation = self.current_generation
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            A = []
            for i in range (self.cell_height):
                A.append([])
                for j in range (self.cell_width):
                    A[i].append(random.randint(0,1))
            return A
        else:
            A = []
            for i in range(self.cell_height):
                A.append([])
                for j in range(self.cell_width):
                    A[i].append(0)
            return A
        pass


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                val = self.grid[i][j]
                if val == 1:
                    colour = pygame.Color('green')
                else:
                    colour = pygame.Color('white')
                pygame.draw.rect(self.screen, colour, (j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= cell[0] + i < self.cell_height and 0 <= cell[1] + j < self.cell_width and (i, j) != (0, 0):
                    neighbours.append(self.grid[cell[0] + i][cell[1] + j])
        return neighbours


    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        A = []
        for i in range (self.cell_height):
            A.append([])
            for j in range (self.cell_width):
                N = self.get_neighbours((i,j))
                count = 0
                for value in N:
                    if value == 1:
                        count += 1

                val = self.grid[i][j]
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


