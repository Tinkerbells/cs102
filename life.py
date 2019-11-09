import random
import pygame
import typing
import copy
import pathlib
from pygame.locals import *
from typing import List, Tuple, Optional

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
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


    def create_grid(self, randomize: bool = False) -> Grid:

        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for x in range(self.rows):
            for y in range(self.cols):
                if randomize:
                    grid[x][y] = random.randint(0, 1)

        return grid

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
                h = cell[0] + i
                w = cell[1] + j

                if 0 <= w < self.cols and 0 <= h < self.rows and (i, j) != (0, 0):
                    neighbours.append(self.curr_generation[h][w])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        next_grid = copy.deepcopy(self.curr_generation)
        for x in range(self.rows):
            for y in range(self.cols):
                cells = self.get_neighbours((x, y))
                count = sum(cells)
                if count == 3:
                    next_grid[x][y] = 1
                elif count != 2 and count != 3:
                    next_grid[x][y] = 0

        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation, self.curr_generation = self.curr_generation, self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.curr_generation == self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        height = 0
        grid = []
        f = open(filename)
        for line in f:
            row = [int(i) for i in line if i != '\n']
            grid.append(row)
            height += 1
        width = len(row)
        start_from_file = GameOfLife((height, width), False)
        start_from_file.prev_generation = GameOfLife.create_grid(start_from_file)
        start_from_file.curr_generation = grid
        f.close()

        return start_from_file

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        for i in range(self.rows):
            for j in range(self.cols):
                f.write(str(self.curr_generation[i][j]))
            f.write('\n')
        f.close()
