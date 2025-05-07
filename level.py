from map import Map
from coin import Coin

class Level:
    def __init__(self):
        self.map = Map(10, 10)
        self.coins = []  # список об'єктів Coin

    def generate_level(self):
        # Примітивна генерація: кілька стін вручну
        self.map.tiles[1][1].is_wall = True
        self.map.tiles[2][3].is_wall = True
        self.map.tiles[4][4].is_wall = True

        # Кілька монет — де немає стін
        for y in range(10):
            for x in range(10):
                if not self.map.is_wall(x, y):
                    self.coins.append(Coin(x, y))