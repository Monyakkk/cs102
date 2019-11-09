# coding=utf-8
import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    colour = pygame.Color('green')
                else:
                    colour = pygame.Color('white')
                pygame.draw.rect(self.screen, colour, (
                j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.draw_lines()

        running = True
        exitflag = 0
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # Пробел ставит игру на паузу

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                x = pos[0] // self.cell_size
                                y = pos[1] // self.cell_size
                                if self.life.curr_generation[y][x] == 0:
                                    self.life.curr_generation[y][x] = 1
                                else:
                                    self.life.curr_generation[y][x] = 0
                                self.draw_grid()
                                pygame.display.flip()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                paused = False
                            if event.type == QUIT:
                                running = False
                                paused = False
                                exitflag = 1

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.life.step()

            # Отрисовка списка клеток
            if exitflag == 0:
                self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

