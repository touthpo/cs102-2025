import os
import sys
from typing import TYPE_CHECKING

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_r

if TYPE_CHECKING:
    from life import GameOfLife
    from ui import UI

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем после добавления пути
try:
    from life import GameOfLife
    from ui import UI
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    # Создаем заглушки для типизации
    import abc

    class UIGame(abc.ABC):
        def __init__(self, life: "GameOfLife") -> None:
            self.life = life

        @abc.abstractmethod
        def run(self) -> None:
            pass


class GUI(UI):
    """
    Графический интерфейс с использованием PyGame.
    """

    def __init__(self, life: "GameOfLife", cell_size: int = 10, speed: int = 10) -> None:
        """
        Инициализация графического интерфейса.
        """
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        # Вычисляем размеры окна
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        # Состояние интерфейса
        self.paused = True

        # Инициализация PyGame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

        # Шрифт для текста
        self.font = pygame.font.Font(None, 24)

        # Цвета
        self.colors = {
            "background": pygame.Color("white"),
            "grid_lines": pygame.Color("black"),
            "cell_alive": pygame.Color("green"),
            "cell_dead": pygame.Color("white"),
            "text": pygame.Color("black"),
            "text_paused": pygame.Color("red"),
        }

    def draw_lines(self) -> None:
        """
        Рисует линии сетки.
        """
        # Вертикальные линии
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.colors["grid_lines"], (x, 0), (x, self.height))

        # Горизонтальные линии
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.colors["grid_lines"], (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Рисует клетки.
        """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                # Вычисляем координаты прямоугольника
                rect_x = x * self.cell_size
                rect_y = y * self.cell_size

                # Выбираем цвет в зависимости от состояния клетки
                color = self.colors["cell_alive"] if self.life.curr_generation[y][x] else self.colors["cell_dead"]

                # Рисуем прямоугольник
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, self.cell_size, self.cell_size))

    def draw_info(self) -> None:
        """
        Отображает информацию о состоянии игры.
        """
        # Поколение
        gen_text = f"Generation: {self.life.generations}"
        gen_surface = self.font.render(gen_text, True, self.colors["text"])
        self.screen.blit(gen_surface, (10, 10))

        # Статус паузы
        if self.paused:
            pause_text = "PAUSED - Click cells to draw, SPACE to continue"
            pause_surface = self.font.render(pause_text, True, self.colors["text_paused"])
            self.screen.blit(pause_surface, (10, 35))

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """
        Обрабатывает клик мыши для рисования клеток.
        """
        x, y = pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size

        # Меняем состояние клетки (только если в пределах сетки)
        if 0 <= grid_x < self.life.cols and 0 <= grid_y < self.life.rows:
            # Переключаем клетку (0 ↔ 1)
            current = self.life.curr_generation[grid_y][grid_x]
            self.life.curr_generation[grid_y][grid_x] = 0 if current else 1

    def run(self) -> None:
        """
        Запускает основной игровой цикл.
        """
        running = True

        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    # Выход по ESC
                    if event.key == K_ESCAPE:
                        running = False

                    # Пауза/продолжение по пробелу
                    elif event.key == K_SPACE:
                        self.paused = not self.paused

                    # Рестарт по R
                    elif event.key == K_r:
                        self.life.curr_generation = self.life.create_grid(randomize=True)
                        self.life.generations = 1

                elif event.type == MOUSEBUTTONDOWN:
                    # Клик мыши - меняем состояние клетки (только на паузе)
                    if event.button == 1 and self.paused:  # Левая кнопка
                        self.handle_mouse_click(event.pos)

            # Обновляем состояние, если не на паузе
            if not self.paused:
                if not self.life.is_max_generations_exceeded and self.life.is_changing:
                    self.life.step()
                else:
                    # Если достигнут лимит поколений или состояние не меняется
                    self.paused = True

            # Отрисовка
            self.screen.fill(self.colors["background"])
            self.draw_grid()
            self.draw_lines()
            self.draw_info()

            # Обновление экрана
            pygame.display.flip()

            # Контроль скорости
            self.clock.tick(self.speed)

        pygame.quit()


# Код для запуска, если файл выполняется напрямую
if __name__ == "__main__":
    # Создаем игру со случайным начальным состоянием
    game = GameOfLife((25, 35), randomize=True, max_generations=500)

    # Создаем GUI
    gui = GUI(game, cell_size=20, speed=10)

    print("Запуск игры...")
    print("Управление: SPACE - пауза, R - рестарт, ESC - выход")

    # Запускаем
    gui.run()
