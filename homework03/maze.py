from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    Удаляет стену в случайном направлении (вверх или вправо) из заданной клетки.
    
    :param grid: лабиринт
    :param coord: координаты клетки (x, y)
    :return: обновленный лабиринт
    """
    x, y = coord
    directions = []
    
    # Проверяем возможные направления (ТОЛЬКО ВВЕРХ ИЛИ ВПРАВО по алгоритму двоичного дерева)
    if x > 1:  # Можно пойти вверх
        directions.append('up')
    if y < len(grid[0]) - 2:  # Можно пойти вправо
        directions.append('right')
    
    # Если есть хотя бы одно возможное направление
    if directions:
        direction = choice(directions)
        
        if direction == 'up':
            # Сносим стену между (x, y) и (x-1, y)
            grid[x-1][y] = " "
        elif direction == 'right':
            # Сносим стену между (x, y) и (x, y+1)
            grid[x][y+1] = " "
    
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    Создает лабиринт алгоритмом двоичного дерева.
    
    :param rows: количество строк
    :param cols: количество столбцов
    :param random_exit: случайные вход/выход если True
    :return: сгенерированный лабиринт
    """
    grid = create_grid(rows, cols)
    
    # ВАЖНО: Создаем пустые клетки в нечетных позициях
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
    
    # ВАЖНО: Применяем алгоритм двоичного дерева ТОЛЬКО к пустым клеткам
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid = remove_wall(grid, (x, y))
    
    # Генерация входа и выхода
    if random_exit:
        # Вход
        x_in = randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        
        # Выход (не совпадающий с входом)
        while True:
            x_out = randint(0, rows - 1)
            y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
            if (x_in, y_in) != (x_out, y_out):
                break
    else:
        # Фиксированные позиции как в тестах
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
    
    # Помечаем вход и выход
    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"
    
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    Находит все точки входа/выхода (клетки с "X").
    
    :param grid: лабиринт
    :return: список координат точек входа/выхода
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    Выполняет один шаг волнового алгоритма.
    
    :param grid: лабиринт с разметкой
    :param k: текущая метка (расстояние)
    :return: обновленный лабиринт
    """
    rows = len(grid)
    cols = len(grid[0])
    new_grid = deepcopy(grid)
    
    # Ищем все клетки с меткой k и распространяем волну
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                # Проверяем соседние клетки
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                
                for ni, nj in neighbors:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        # Если соседняя клетка пустая (0 или " ")
                        if grid[ni][nj] == 0 or (isinstance(grid[ni][nj], str) and grid[ni][nj] == " "):
                            new_grid[ni][nj] = k + 1
                        # Если это выход с "X" (кроме начальной точки)
                        elif grid[ni][nj] == "X" and new_grid[ni][nj] == "X":
                            # Находим, есть ли уже другой выход
                            exits = get_exits(grid)
                            # Если это не начальный выход
                            if (ni, nj) != exits[0]:
                                new_grid[ni][nj] = k + 1
    
    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Восстанавливает кратчайший путь от выхода к входу по размеченному лабиринту.
    
    :param grid: лабиринт с разметкой волнового алгоритма
    :param exit_coord: координаты выхода
    :return: путь (список координат) или None
    """
    x, y = exit_coord
    
    # Если выход не достижим
    if not isinstance(grid[x][y], int) or grid[x][y] <= 0:
        return None
    
    path = []
    current_x, current_y = x, y
    current_value = grid[x][y]
    
    # Идем от выхода ко входу
    while current_value > 1:
        path.append((current_x, current_y))
        
        # Ищем соседнюю клетку с меньшим значением
        neighbors = [
            (current_x-1, current_y),
            (current_x+1, current_y), 
            (current_x, current_y-1),
            (current_x, current_y+1)
        ]
        
        found = False
        for nx, ny in neighbors:
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if isinstance(grid[nx][ny], int) and grid[nx][ny] == current_value - 1:
                    current_x, current_y = nx, ny
                    current_value = grid[nx][ny]
                    found = True
                    break
        
        if not found:
            break
    
    # Добавляем последнюю клетку (вход)
    path.append((current_x, current_y))
    
    # ВАЖНО: Тесты ожидают путь от входа к выходу, а не наоборот!
    # Реверсируем путь
    return list(reversed(path))


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет, окружена ли клетка стенами (является ли тупиком).
    
    :param grid: лабиринт
    :param coord: координаты клетки (x, y)
    :return: True если клетка окружена, иначе False
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])
    
    # Если координаты вне границ
    if x < 0 or x >= rows or y < 0 or y >= cols:
        return True
    
    # Если это стена
    if grid[x][y] == "■":
        return True
    
    # Проверяем соседей
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    wall_count = 0
    
    for nx, ny in neighbors:
        # Если сосед за границей - считаем как стену
        if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
            wall_count += 1
        # Если сосед - стена
        elif grid[nx][ny] == "■":
            wall_count += 1
    
    # Для клеток на границе: если 3 стены - тупик
    # Для внутренних клеток: если 4 стены - тупик
    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        return wall_count >= 3
    else:
        return wall_count == 4


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Находит кратчайший путь в лабиринте между входом и выходом.
    
    :param grid: лабиринт
    :return: (лабиринт с разметкой, путь) или (лабиринт, None) если пути нет
    """
    # Создаем копию для разметки
    marked_grid = deepcopy(grid)
    
    # Находим входы/выходы
    exits = get_exits(grid)
    
    if len(exits) < 2:
        return marked_grid, None
    
    # Начинаем волновой алгоритм от ПЕРВОГО выхода (как в тестах)
    start_x, start_y = exits[0]
    
    # Инициализируем: вход = 1, остальные = 0
    for i in range(len(marked_grid)):
        for j in range(len(marked_grid[0])):
            if marked_grid[i][j] == " ":
                marked_grid[i][j] = 0
            elif marked_grid[i][j] == "X":
                if (i, j) == (start_x, start_y):
                    marked_grid[i][j] = 1
                else:
                    marked_grid[i][j] = 0
    
    # Применяем волновой алгоритм
    k = 1
    exit_coord = exits[1]
    
    # Пока выход не достигнут и есть клетки для обработки
    while True:
        current_value = marked_grid[exit_coord[0]][exit_coord[1]]
        
        # Если выход достигнут
        if isinstance(current_value, int) and current_value > 0:
            break
        
        # Выполняем шаг
        marked_grid = make_step(marked_grid, k)
        k += 1
        
        # Проверяем, есть ли еще клетки для обработки
        has_more = False
        for row in marked_grid:
            for cell in row:
                if cell == k:
                    has_more = True
                    break
            if has_more:
                break
        
        if not has_more:
            break
    
    # Восстанавливаем путь
    exit_value = marked_grid[exit_coord[0]][exit_coord[1]]
    if not isinstance(exit_value, int) or exit_value <= 0:
        return marked_grid, None
    
    path = shortest_path(marked_grid, exit_coord)
    
    return marked_grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    Добавляет путь в лабиринт.
    
    :param grid: лабиринт
    :param path: путь (список координат)
    :return: лабиринт с отмеченным путем
    """
    if path:
        # Если path - одиночная координата
        if isinstance(path, tuple) and len(path) == 2:
            i, j = path
            grid[i][j] = "X"
        # Если path - список координат
        elif isinstance(path, list):
            for i, j in path:
                grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
