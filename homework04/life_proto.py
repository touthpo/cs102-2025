import random
from typing import List, Tuple

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_r

Cell = Tuple[int, int]
Cells = List[Cell]
Grid = List[List[int]]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed

        self.cell_width = width // cell_size
        self.cell_height = height // cell_size

        self.grid = self.create_grid(randomize=True)

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game of Life - Prototype")
        self.clock = pygame.time.Clock()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for _ in range(self.cell_height):
            row = []
            for _ in range(self.cell_width):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        neighbours = []

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
                    neighbours.append((nx, ny))

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = []

        for y in range(self.cell_height):
            new_row = []
            for x in range(self.cell_width):
                neighbours = self.get_neighbours((x, y))
                live_neighbours = sum(1 for nx, ny in neighbours if self.grid[ny][nx] == 1)

                current = self.grid[y][x]

                if current == 1:
                    if live_neighbours in [2, 3]:
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if live_neighbours == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)

            new_grid.append(new_row)

        return new_grid

    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                rect_x = x * self.cell_size
                rect_y = y * self.cell_size

                color = pygame.Color("green") if self.grid[y][x] else pygame.Color("white")
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, self.cell_size, self.cell_size))

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.grid = self.get_next_generation()

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()

            self.clock.tick(self.speed)

        pygame.quit()

        def some_function():
            """
            Returns
            -------
            out : Cells
                Список соседних клеток, в котором каждая позиция - 0 или 1.
            """
            pass


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
