from life import GameOfLife
from life_console import Console

if __name__ == "__main__":
    life = GameOfLife((20, 40), randomize=True, max_generations=50)
    console = Console(life)
    console.run()
