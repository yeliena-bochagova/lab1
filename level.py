import random
from map import Map
from coin import Coin
from mazelib import Maze
from mazelib.generate.Prims import Prims

def generate_maze(width, height):
    maze = Maze()
    maze.generator = Prims(width, height)
    maze.generate()
    return maze.grid

def add_extra_exits(maze_grid, probability=0.3):
    """
    Додаємо додаткові виходи, видаляючи деякі стіни,
    щоб лабіринт мав більше проходів.
    """
    height = len(maze_grid)
    width = len(maze_grid[0])
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if maze_grid[y][x] == 1:
                # Перевірка горизонтальних сусідів
                if maze_grid[y][x - 1] == 0 and maze_grid[y][x + 1] == 0:
                    if random.random() < probability:
                        maze_grid[y][x] = 0
                # Перевірка вертикальних сусідів
                if maze_grid[y - 1][x] == 0 and maze_grid[y + 1][x] == 0:
                    if random.random() < probability:
                        maze_grid[y][x] = 0
    return maze_grid

class Level:
    def __init__(self):
        # Створюємо більшу карту, наприклад 20x20
        self.map = Map(10, 10)
        self.coins = []  # список об’єктів Coin

    def generate_level(self):
        # Генеруємо базовий лабіринт за алгоритмом Пріма
        maze_grid = generate_maze(self.map.width, self.map.height)
        # Додаємо додаткові виходи, щоб лабіринт не був суцільно замкнутим
        maze_grid = add_extra_exits(maze_grid, probability=0.3)

        # Заповнюємо поле на основі лабіринту, але не задаємо стіни по краях
        for y in range(self.map.height):
            for x in range(self.map.width):
                # Якщо клітинка знаходиться на краю, вона завжди буде прохідною
                if x == 0 or y == 0 or x == self.map.width - 1 or y == self.map.height - 1:
                    self.map.tiles[y][x].is_wall = False
                else:
                    self.map.tiles[y][x].is_wall = (maze_grid[y][x] == 1)

        # Розташовуємо монети у клітинках, де немає стін
        for y in range(self.map.height):
            for x in range(self.map.width):
                if not self.map.is_wall(x, y):
                    self.coins.append(Coin(x, y))