from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd
import copy


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    row, col = coord
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        if grid[row][col] != "X":
            grid[row][col] = " "
    return grid

def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    for x in range(1, rows - 1, 2):
        for y in range(1, cols - 1, 2):
            possible_directions = []
            if x - 2 >= 1: 
                possible_directions.append("up")
            if y + 2 <= cols - 2:
                possible_directions.append("right")
            if possible_directions:
                direction = choice(possible_directions)
                if direction == "up":
                    grid[x - 1][y] = " "
                elif direction == "right":
                    grid[x][y + 1] = " "
            else:
                if x - 2 >= 1:
                    grid[x - 1][y] = " "
                elif y + 2 <= cols - 2:
                    grid[x][y + 1] = " "
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                directions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in directions:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == 0 and grid[ni][nj] != '■':
                            grid[ni][nj] = k + 1
    
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    exit_row, exit_col = exit_coord
    if not (0 <= exit_row < len(grid) and 0 <= exit_col < len(grid[0])):
        return None
    if grid[exit_row][exit_col] == 0 or grid[exit_row][exit_col] == 'X':
        return None
    path_length = grid[exit_row][exit_col]
    path = [exit_coord]
    current_row, current_col = exit_coord
    current_value = path_length
    while current_value > 1:
        found_next = False
        directions = [
            (current_row - 1, current_col),
            (current_row + 1, current_col),
            (current_row, current_col - 1),
            (current_row, current_col + 1)
        ]
        
        for next_row, next_col in directions:
            if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
                if grid[next_row][next_col] == current_value - 1:
                    path.append((next_row, next_col))
                    current_row, current_col = next_row, next_col
                    current_value -= 1
                    found_next = True
                    break
        if not found_next:
            print(f"Ошибка: не могу найти клетку со значением {current_value - 1}")
            return None
    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    row, col = coord
    rows = len(grid)
    cols = len(grid[0])
    walls = 0
    if row == 0 or grid[row - 1][col] == "■":
        walls += 1
    if row == rows - 1 or grid[row + 1][col] == "■":
        walls += 1
    if col == 0 or grid[row][col - 1] == "■":
        walls += 1
    if col == cols - 1 or grid[row][col + 1] == "■":
        walls += 1
    is_corner = (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1)
    is_border = row == 0 or row == rows - 1 or col == 0 or col == cols - 1
    if is_corner:
        return walls >= 3
    elif is_border:
        if walls >= 3:
            return True
        elif walls == 2:
            return False
        else:
            return True
    else:
        return walls >= 3


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    maze = copy.deepcopy(grid)
    exits = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "X":
                exits.append((i, j))
    if len(exits) != 2:
        return maze, None
    start, end = exits[0], exits[1]
    if encircled_exit(maze, end):
        return maze, None
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == " ":
                maze[i][j] = 0
            elif maze[i][j] == "X":
                if (i, j) == start:
                    maze[i][j] = 1
                else:
                    maze[i][j] = 0
    current_step = 1
    while maze[end[0]][end[1]] == 0:
        cells_to_process = []
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == current_step:
                    cells_to_process.append((i, j))
        if not cells_to_process:
            return maze, None
        for i, j in cells_to_process:
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if (0 <= ni < len(maze) and 
                    0 <= nj < len(maze[0]) and 
                    maze[ni][nj] == 0):
                    maze[ni][nj] = current_step + 1
        current_step += 1
        if current_step > len(maze) * len(maze[0]):
            return maze, None
    path = []
    current = end
    while maze[current[0]][current[1]] != 1:
        path.append(current)
        i, j = current
        current_value = maze[i][j]
        found = False
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if (0 <= ni < len(maze) and 
                0 <= nj < len(maze[0]) and 
                maze[ni][nj] == current_value - 1):
                current = (ni, nj)
                found = True
                break
        if not found:
            return maze, None
    path.append(current)
    path.reverse()
    return maze, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid

def print_maze_pretty(grid: List[List[Union[str, int]]], title: str = "Лабиринт"):
    """Красивая печать лабиринта с рамкой."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    print(f"\n╔{'═' * (cols * 2 + 1)}╗")
    print(f"║ {title:^{cols * 2 - 1}} ║")
    print(f"╠{'═' * (cols * 2 + 1)}╣")
    
    for i, row in enumerate(grid):
        # Добавляем номер строки слева
        row_str = f"{i:2d} │ "
        
        for j, cell in enumerate(row):
            # Разные символы для разных типов клеток
            if cell == "■":
                row_str += "██"  # Стена
            elif cell == " ":
                row_str += "  "  # Проход
            elif cell == "X":
                row_str += "╳╳"  # Вход/выход
            elif cell == "•" or cell == "*":
                row_str += "∙∙"  # Путь
            elif isinstance(cell, int) and cell > 0:
                row_str += f"{cell:2d}"  # Число
            else:
                row_str += "  "
        
        row_str += " │"
        print(row_str)
    
    print(f"╚{'═' * (cols * 2 + 1)}╝")
    
    # Легенда
    print("  Легенда: ██ - стена,   - проход, ╳╳ - вход/выход, ∙∙ - путь")


if __name__ == "__main__":
    print("=" * 60)
    print("ГЕНЕРАЦИЯ И ОБХОД ЛАБИРИНТА - ТЕРМИНАЛЬНАЯ ВЕРСИЯ")
    print("=" * 60)
    
    # Генерация лабиринта
    print("\n1. Генерация лабиринта 15x15...")
    GRID = bin_tree_maze(15, 15, random_exit=True)
    print_maze_pretty(GRID, "Сгенерированный лабиринт")
    
    # Поиск пути
    print("\n2. Поиск кратчайшего пути...")
    MAZE, PATH = solve_maze(GRID)
    
    if PATH:
        print(f"   ✓ Путь найден! Длина: {len(PATH)} шагов")
        
        # Отображаем путь
        MAZE_WITH_PATH = add_path_to_grid(GRID, PATH)
        print_maze_pretty(MAZE_WITH_PATH, "Лабиринт с кратчайшим путем")
        
        # Показываем координаты пути
        print("\n3. Координаты пути:")
        print("   " + "-" * 30)
        for i in range(0, len(PATH), 5):
            chunk = PATH[i:i+5]
            coords = ", ".join([f"({r},{c})" for r, c in chunk])
            print(f"   Шаги {i:2d}-{i+len(chunk)-1:2d}: {coords}")
        
        # Статистика
        flat_grid = [cell for row in GRID for cell in row]
        print("\n4. Статистика:")
        print(f"   • Размер: 15x15 (225 клеток)")
        print(f"   • Стен: {flat_grid.count('■')}")
        print(f"   • Проходов: {flat_grid.count(' ')}")
        print(f"   • Длина пути: {len(PATH)} шагов")
        print(f"   • Заполнение: {(len(PATH)/225)*100:.1f}% лабиринта")
        
    else:
        print("   ✗ Путь не найден!")
        print_maze_pretty(MAZE, "Размеченный лабиринт (пути нет)")

if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))


