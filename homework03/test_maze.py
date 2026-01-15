import unittest

from maze import *


class TestMazeSolver(unittest.TestCase):

    def test_create_grid(self):
        grid = create_grid(5, 5)
        self.assertEqual(len(grid), 5)
        self.assertEqual(len(grid[0]), 5)
        self.assertEqual(grid[0][0], "■")

    def test_get_exits(self):
        grid = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["X", "■", "■", "■", "X"],
        ]
        exits = get_exits(grid)
        self.assertEqual(len(exits), 2)
        self.assertIn((4, 0), exits)
        self.assertIn((4, 4), exits)

    def test_bin_tree_maze_small(self):
        maze = bin_tree_maze(5, 5, random_exit=False)
        exits = get_exits(maze)
        self.assertEqual(len(exits), 2)

    def test_solve_maze_small(self):
        maze = bin_tree_maze(7, 7, random_exit=False)
        solved_maze, path = solve_maze(maze)
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 1)


if __name__ == "__main__":
    unittest.main() 
