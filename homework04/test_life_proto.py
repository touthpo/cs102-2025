import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from life_proto import GameOfLife


class TestGameOfLifeProto(unittest.TestCase):

    def test_create_grid(self):
        game = GameOfLife(100, 100, 10)

        self.assertEqual(game.cell_width, 10)
        self.assertEqual(game.cell_height, 10)
        self.assertEqual(len(game.grid), 10)
        self.assertEqual(len(game.grid[0]), 10)

    def test_get_neighbours(self):
        game = GameOfLife(30, 30, 10)

        neighbours = game.get_neighbours((1, 1))
        self.assertEqual(len(neighbours), 8)

        neighbours = game.get_neighbours((0, 0))
        self.assertEqual(len(neighbours), 3)

    def test_next_generation_empty(self):
        game = GameOfLife(30, 30, 10)
        game.grid = game.create_grid(randomize=False)

        next_gen = game.get_next_generation()

        for row in next_gen:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_single_cell_dies(self):
        game = GameOfLife(30, 30, 10)
        game.grid = game.create_grid(randomize=False)

        game.grid[1][1] = 1

        next_gen = game.get_next_generation()

        self.assertEqual(next_gen[1][1], 0)


if __name__ == "__main__":
    unittest.main()
