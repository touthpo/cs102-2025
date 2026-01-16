"""
ui.py - Абстрактный базовый класс для интерфейсов
"""

import abc
from typing import TYPE_CHECKING

# Для аннотаций типов используем TYPE_CHECKING
if TYPE_CHECKING:
    from life import GameOfLife


class UI(abc.ABC):
    """
    Абстрактный базовый класс для интерфейсов игры.
    """

    def __init__(self, life: "GameOfLife") -> None:  # Строковая аннотация
        """
        Инициализация интерфейса.

        Args:
            life: Объект игры
        """
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        """Запускает интерфейс."""
        pass
