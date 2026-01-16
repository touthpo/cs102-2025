import os
import pathlib
import random
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from life import GameOfLife


class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        random.seed(42)

    def test_create_grid_random(self):
        game = GameOfLife((10, 10), randomize=True)

        self.assertEqual(len(game.curr_generation), 10)
        self.assertEqual(len(game.curr_generation[0]), 10)

        flat_grid = [cell for row in game.curr_generation for cell in row]
        self.assertIn(0, flat_grid)
        self.assertIn(1, flat_grid)

    def test_create_grid_empty(self):
        game = GameOfLife((5, 5), randomize=False)

        for row in game.curr_generation:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_get_neighbours_center(self):
        game = GameOfLife((5, 5), randomize=False)
        neighbours = game.get_neighbours((2, 2))

        self.assertEqual(len(neighbours), 8)

        expected = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        self.assertEqual(set(neighbours), set(expected))

    def test_get_neighbours_corner(self):
        game = GameOfLife((5, 5), randomize=False)
        neighbours = game.get_neighbours((0, 0))

        self.assertEqual(len(neighbours), 3)

        expected = [(1, 0), (0, 1), (1, 1)]
        self.assertEqual(set(neighbours), set(expected))

    def test_step_generation_counter(self):
        game = GameOfLife((5, 5), randomize=True)

        initial_generation = game.generations
        game.step()

        self.assertEqual(game.generations, initial_generation + 1)

    def test_is_changing(self):
        game = GameOfLife((3, 3), randomize=False)

        self.assertFalse(game.is_changing)

        game.curr_generation[0][1] = 1
        game.curr_generation[1][1] = 1
        game.curr_generation[2][1] = 1

        game.step()

        self.assertTrue(game.is_changing)

    def test_max_generations(self):
        game = GameOfLife((5, 5), randomize=True, max_generations=5)

        for _ in range(3):
            game.step()
            self.assertFalse(game.is_max_generations_exceeded)

        game.step()
        self.assertTrue(game.is_max_generations_exceeded)

        game.step()
        self.assertTrue(game.is_max_generations_exceeded)

    def test_save_load(self):
        game = GameOfLife((3, 3), randomize=False)
        game.curr_generation = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

        test_file = pathlib.Path("test_save.txt")
        game.save(test_file)

        loaded_game = GameOfLife.from_file(test_file)

        self.assertEqual(loaded_game.curr_generation, game.curr_generation)

        test_file.unlink()

    def test_blinker_pattern(self):
        game = GameOfLife((5, 5), randomize=False)

        game.curr_generation[1][2] = 1
        game.curr_generation[2][2] = 1
        game.curr_generation[3][2] = 1

        original_state = [row[:] for row in game.curr_generation]

        game.step()

        expected_state = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        self.assertNotEqual(game.curr_generation, original_state)

        self.assertEqual(game.curr_generation[2][1:4], [1, 1, 1])


if __name__ == "__main__":
    unittest.main()
