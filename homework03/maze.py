from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)

    for i in range(1, rows - 1, 2):
        for j in range(1, cols - 1, 2):
            grid[i][j] = " "

    for i in range(1, rows - 1, 2):
        for j in range(1, cols - 1, 2):
            directions = []

            if i > 1:
                directions.append("up")

            if j < cols - 3:
                directions.append("right")

            if directions:
                direction = choice(directions)

                if direction == "up":
                    grid[i - 1][j] = " "
                elif direction == "right":
                    grid[i][j + 1] = " "

    if not random_exit:
        grid[rows - 1][0] = "X"
        if rows > 1 and grid[rows - 2][0] == "■":
            grid[rows - 2][0] = " "

        grid[0][cols - 1] = "X"
        if cols > 1 and grid[0][cols - 2] == "■":
            grid[0][cols - 2] = " "

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    if grid is None:
        return []

    exits = []
    rows = len(grid)

    for i in range(rows):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                exits.append((i, j))

    return exits


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    if grid is None:
        return True

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    passable = 0

    if x > 0 and grid[x - 1][y] != "■":
        passable += 1
    if x < rows - 1 and grid[x + 1][y] != "■":
        passable += 1
    if y > 0 and grid[x][y - 1] != "■":
        passable += 1
    if y < cols - 1 and grid[x][y + 1] != "■":
        passable += 1

    return passable == 0


def bfs_find_path(grid, start, end):
    if grid is None:
        return None

    rows = len(grid)
    cols = len(grid[0])

    visited = [[False] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]

    queue = [start]
    visited[start[0]][start[1]] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.pop(0)

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[x][y]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if (grid[nx][ny] == " " or grid[nx][ny] == "X") and not visited[nx][ny]:
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))

    return None


def solve_maze(grid):
    if grid is None:
        return None, None

    exits = get_exits(grid)

    if len(exits) < 2:
        return grid, None

    start, end = exits[0], exits[1]

    path = bfs_find_path(grid, start, end)

    return grid, path


def add_path_to_grid(grid, path):
    if grid is None or path is None:
        return grid

    for x, y in path:
        if grid[x][y] != "X":
            grid[x][y] = "•"

    return grid


def remove_wall(grid, coord):
    if grid is None:
        return grid

    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "

    return grid


if __name__ == "__main__":
    print("=== Тестирование ===")

    try:
        GRID = bin_tree_maze(15, 15, random_exit=False)

        if GRID is None:
            print("Ошибка: bin_tree_maze вернул None")
        else:
            print("Лабиринт сгенерирован успешно")
            print(f"Размер: {len(GRID)}x{len(GRID[0])}")

            exits = get_exits(GRID)
            print(f"Найдено выходов: {len(exits)}")

            MAZE, PATH = solve_maze(GRID)

            if PATH:
                print(f"Путь найден! Длина: {len(PATH)}")
                MAZE = add_path_to_grid(MAZE, PATH)
            else:
                print("Путь не найден")

    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        import traceback

        traceback.print_exc()
