import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
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
        super().__init__(life)

    def draw_lines(self):
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

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

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.life.curr_generation = self.life.create_grid(randomize=True)

        running = True
        paused = True
        n = 0
        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    x = click_pos[0] // self.cell_size
                    y = click_pos[1] // self.cell_size
                    self.grid[y][x] = (self.grid[y][x] + 1) % 2
                if event.type == KEYDOWN and event.key == K_SPACE:
                    paused = False
                    n += 1
                if event.type == KEYDOWN and event.key == K_SPACE and n % 2 == 0:
                    paused = True
            self.draw_lines()
            self.draw_grid()

            if paused == False:
                self.grid = self.get_next_generation()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
