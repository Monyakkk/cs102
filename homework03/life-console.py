import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range (self.life.rows):
            for j in range (self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')
                else:
                    screen.addstr(i + 1, j + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        while True:
            if self.life.is_max_generations_exceeded == True or self.life.is_changing == False:
                break
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
        curses.endwin()
