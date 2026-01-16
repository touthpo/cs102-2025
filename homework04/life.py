import pathlib
import random
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[Cell]
Grid = List[List[int]]


class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[float] = None) -> None:
        self.rows, self.cols = size
        self.max_generations = float("inf") if max_generations is None else max_generations
        self.generations = 1

        self.prev_generation = self.create_grid(False)
        self.curr_generation = self.create_grid(randomize)

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
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

                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    neighbours.append((nx, ny))

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = []

        for y in range(self.rows):
            new_row = []
            for x in range(self.cols):
                neighbours = self.get_neighbours((x, y))

                live_neighbours = sum(1 for nx, ny in neighbours if self.curr_generation[ny][nx] == 1)

                current = self.curr_generation[y][x]

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

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]

        self.curr_generation = self.get_next_generation()

        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines if line.strip()]

        grid = []
        for line in lines:
            row = [int(ch) for ch in line]
            grid.append(row)

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for row in self.curr_generation:
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
