import curses
import keyboard
import datetime
import time

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
        running = True
   
        while running:
            a=[]
            start = datetime.datetime.now()
            while True:
                if  start.second+1 <= datetime.datetime.now().second:
                    break
                try:
                    if keyboard.is_pressed('q'):
                        a.append('q')
                except Exception:
                    pass
                try:
                    if keyboard.is_pressed('s'):
                        a.append('s')
                except Exception:
                    pass


            for event in a:
                if event == 'q':
                    running = False
                if event == 's':
                    self.life.save("save.txt")    

                            
            if self.life.is_max_generations_exceeded == True or self.life.is_changing == False:
                running = False
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
        curses.endwin()

if __name__ == "__main__":
    life = GameOfLife((24, 50), True, max_generations=200)
    ui = Console(life)
    ui.run()

