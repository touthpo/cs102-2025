import tkinter as tk
from typing import List, Union
from tkinter import ttk, messagebox
from maze import bin_tree_maze, solve_maze, add_path_to_grid


def draw_cell(x: int, y: int, color: str, size: int = 10) -> None:
    """Рисует одну клетку лабиринта."""
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color, outline="gray")


def draw_maze(grid: List[List[Union[str, int]]], size: int = 10) -> None:
    """Рисует весь лабиринт."""
    canvas.delete("all") 
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " " or cell == 0:
                color = 'white'
            elif cell == "■":
                color = 'black'
            elif cell == "X":
                color = "yellow"
            elif cell == "•" or cell == "*": 
                color = "green" 
            else:
                color = 'white'  
            draw_cell(y, x, color, size)


def show_solution() -> None:
    """Показывает решение лабиринта."""
    global GRID, CELL_SIZE
    maze_copy = [row[:] for row in GRID]
    solved_maze, path = solve_maze(maze_copy)
    if path:
        maze_with_path = add_path_to_grid(GRID, path)
        draw_maze(maze_with_path, CELL_SIZE)
        messagebox.showinfo("Решение найдено", 
                           f"Длина пути: {len(path)} шагов\n"
                           f"Путь отображен зеленым цветом")
    else:
        messagebox.showinfo("Решение не найдено", 
                           "Путь из входа в выход не существует")

def generate_new_maze() -> None:
    global GRID, N, M
    path_found = False
    attempts = 0
    while not path_found and attempts < 10:
        GRID = bin_tree_maze(N, M, random_exit=True)
        maze_copy = [row[:] for row in GRID]
        _, path = solve_maze(maze_copy)
        
        if path:
            path_found = True
        else:
            attempts += 1
    draw_maze(GRID, CELL_SIZE)
    if path_found:
        status_label.config(text=f"Лабиринт {N}x{M}. Путь гарантирован.")
    else:
        status_label.config(text=f"Лабиринт {N}x{M}. Путь может отсутствовать.")

if __name__ == "__main__":
    global GRID, CELL_SIZE, N, M, canvas, status_label
    N, M = 25, 35
    CELL_SIZE = 15
    GRID = bin_tree_maze(N, M, random_exit=True)
    window = tk.Tk()
    window.title('Генератор и решатель лабиринтов')
    window.geometry(f"{M * CELL_SIZE + 200}x{N * CELL_SIZE + 200}")
    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE, bg='white')
    canvas.pack(pady=10)
    control_frame = tk.Frame(window)
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Новый лабиринт", 
              command=generate_new_maze, bg="lightblue", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Найти путь", 
              command=show_solution, bg="lightgreen", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Выход", 
              command=window.quit, bg="lightcoral", width=15).pack(side=tk.LEFT, padx=5)
    status_label = tk.Label(window, text=f"Лабиринт {N}x{M}. Нажмите 'Найти путь' для решения.", 
                           relief=tk.SUNKEN, bd=1)
    status_label.pack(fill=tk.X, padx=20, pady=5)
    info_label = tk.Label(window, 
                         text="Цвета: черный - стены, желтый - вход/выход, зеленый - путь", 
                         fg="gray")
    info_label.pack(pady=5)
    draw_maze(GRID, CELL_SIZE)
    window.mainloop()
 

