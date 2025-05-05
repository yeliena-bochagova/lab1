from tile import Tile

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(width)] for _ in range(height)]

    def is_wall(self, x, y):
        """Перевірка, чи є клітинка стіною"""
        return self.tiles[y][x].is_wall

    def print_map(self):
        """Друк карти в консоль"""
        for row in self.tiles:
            print("".join(["#" if tile.is_wall else "." for tile in row]))