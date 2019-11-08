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

    def create_grid(self, randomize: bool = True):
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
        grid2 = []
        self.grid = [[grid2 for i in range(self.cell_width)] for j in range(self.cell_height)]

        for x in range(self.cell_height):
            for y in range(self.cell_width):
                if randomize == False:
                    self.grid[x][y] = 0
                else:
                    self.grid[x][y] = random.randint(0, 1)

        return self.grid

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
        position_x = cell[0]
        position_y = cell[1]
        cells = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= position_x + x < self.cell_width and 0 <= position_y + y < self.cell_height and (x, y) != (
                        0, 0):
                    cells.append(self.grid[position_x + x][position_y + y])

            return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        self.generations += 1
        second_grid = copy.deepcopy(self.grid)
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                cell = [x, y]
                if len(self.get_neighbours(cell)) == 3:
                    second_grid[x][y] = 1
                if len(self.get_neighbours(cell)) < 2 and len(self.get_neighbours(cell)) > 3:
                    second_grid[x][y] = 0

        return second_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        i = bool
        if self.generations > self.max_generations:
            i = True
        else:

            i = False
            return i

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        i = bool
        if self.prev_generation != self.curr_generation:
            i = True
        else:

            i = False
        return i

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
        game.prev_generation = grid
        f.close()

        return start_from_file

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f=open(filename,'w')
        for i in range(self.rows):
            for j in range(self.cols):
                f.write(str(self.curr_generation[i][j]))
            f.write('\n')
        f.close()








