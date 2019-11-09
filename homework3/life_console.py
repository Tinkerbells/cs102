import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        top_border = '+%s+' % (self.life.cols * '-')

        screen.addstr(0, 0, top_border)

        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')

        screen.addstr(self.life.rows + 1, 0, top_border)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """

        grid = self.life.curr_generation

        for row in range(self.life.rows):
            for col in range(self.life.cols):
                screen.addstr(row + 1, col + 1, '*' if grid[row][col] else ' ')

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while (
                self.life.is_changing and not self.life.is_max_generations_exceeded
        ) and running:
            try:
                screen.clear()

                self.draw_borders(screen)
                self.draw_grid(screen)

                self.life.step()

                screen.refresh()
                time.sleep(0.5)

            except KeyboardInterrupt:
                running = False

        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)

    ui = Console(life)
    ui.run()
