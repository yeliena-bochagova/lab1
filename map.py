from tile import Tile

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(width)] for _ in range(height)]

    def load_map(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.height = len(lines)
            self.width = len(lines[0].strip())
            self.tiles = []
            for line in lines:
                row = []
                for char in line.strip():
                    if char == '1':
                        row.append(Tile(is_wall=True))
                    else:
                        row.append(Tile(is_wall=False))
                self.tiles.append(row)

    def is_wall(self, x, y):
        x = int(x)
        y = int(y)
        # Перевіряємо, чи координати знаходяться в межах карти
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        return self.tiles[y][x].is_wall