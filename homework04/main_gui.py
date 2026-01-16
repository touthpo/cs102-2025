from life import GameOfLife
from life_gui import GUI

if __name__ == "__main__":
    # Вариант 1: Случайное начальное состояние
    life = GameOfLife((48, 64), randomize=True, max_generations=1000)

    # Вариант 2: Загрузка из файла
    # life = GameOfLife.from_file('tests/glider.txt')

    gui = GUI(life, cell_size=15, speed=10)
    gui.run()
