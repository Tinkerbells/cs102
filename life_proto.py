import random
import pygame
import typing
import copy
from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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

    def draw_lines(self):
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.create_grid()
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

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

    def draw_grid(self):
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (
                        j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                        j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

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
        second_grid = copy.deepcopy(self.grid)
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                cell =[x, y]
                if len(self.get_neighbours(cell)) == 3:
                    second_grid[x][y] = 1
                if len(self.get_neighbours(cell)) < 2 and len(self.get_neighbours(cell)) > 3:
                    second_grid[x][y] = 0

        return second_grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
