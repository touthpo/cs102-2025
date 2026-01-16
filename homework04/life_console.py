import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from life import GameOfLife
    from ui import UI

# Добавляем путь к текущей директории для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем после добавления пути
try:
    import curses

    from ui import UI
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    sys.exit(1)


class Console(UI):
    """
    Консольный интерфейс с использованием curses.
    """

    def __init__(self, life: "GameOfLife") -> None:
        """
        Инициализация консольного интерфейса.

        Args:
            life: Объект игры
        """
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """
        Отображает рамку вокруг игрового поля.
        """
        # Верхняя и нижняя границы
        for x in range(self.life.cols + 2):
            try:
                screen.addch(0, x, "-")
                screen.addch(self.life.rows + 1, x, "-")
            except curses.error:
                pass

        # Боковые границы
        for y in range(1, self.life.rows + 1):
            try:
                screen.addch(y, 0, "|")
                screen.addch(y, self.life.cols + 1, "|")
            except curses.error:
                pass

        # Углы
        try:
            screen.addch(0, 0, "+")
            screen.addch(0, self.life.cols + 1, "+")
            screen.addch(self.life.rows + 1, 0, "+")
            screen.addch(self.life.rows + 1, self.life.cols + 1, "+")
        except curses.error:
            pass

    def draw_grid(self, screen) -> None:
        """
        Отображает состояние клеток.
        """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                try:
                    char = "█" if self.life.curr_generation[y][x] else " "
                    screen.addch(y + 1, x + 1, char)
                except curses.error:
                    pass  # Игнорируем ошибки на границах

    def run(self) -> None:
        """
        Запускает консольный интерфейс.
        """
        # Инициализация curses
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        try:
            # Настраиваем цвета
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            running = True
            while running:
                # Очищаем экран
                screen.clear()

                # Отображаем информацию
                info = f"Game of Life | Generation: {self.life.generations}"
                if self.life.max_generations != float("inf"):
                    info += f" / {int(self.life.max_generations)}"

                info += " | Press 'q' to quit"
                screen.addstr(0, 0, info)

                # Рисуем поле
                self.draw_borders(screen)
                self.draw_grid(screen)

                # Обновляем экран
                screen.refresh()

                # Выполняем шаг игры
                if not self.life.is_max_generations_exceeded and self.life.is_changing:
                    self.life.step()

                # Ожидаем ввод (100 мс)
                screen.timeout(100)
                key = screen.getch()

                # Выход по 'q'
                if key == ord("q"):
                    running = False

        finally:
            # Восстанавливаем терминал
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()


# Код для запуска, если файл выполняется напрямую
if __name__ == "__main__":
    from life import GameOfLife

    # Создаем игру для демонстрации
    life = GameOfLife((15, 30), randomize=True, max_generations=50)
    console = Console(life)
    console.run()
