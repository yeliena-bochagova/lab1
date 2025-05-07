import random

class Ghost:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.speed = 1  # Фіксований крок для руху

    def move_random(self, map, ghosts):
        """Випадковий рух привида по сітці, щоб не наближатися до інших."""
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)  # Перемішуємо напрями для випадковості

        for direction in directions:
            new_x, new_y = self.x, self.y

            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1

            # Перевіряємо, чи нова позиція не є стіною
            if map.is_wall(new_x, new_y):
                continue

            # Перевіряємо, чи нова позиція не знаходиться занадто близько до інших привидів
            too_close = any(abs(new_x - g.x) + abs(new_y - g.y) < 2 for g in ghosts if g != self)

            if not too_close:
                self.x, self.y = new_x, new_y
                break  # Виходимо з циклу, знайшовши допустимий рух

    def chase_player(self, player, map):
        """Привид рухається до гравця (простий алгоритм), завжди цілочисельним кроком."""
        dx = player.x - self.x
        dy = player.y - self.y

        if abs(dx) > abs(dy):
            new_x = self.x + (1 if dx > 0 else -1)
            if not map.is_wall(new_x, self.y):
                self.x = new_x
        else:
            new_y = self.y + (1 if dy > 0 else -1)
            if not map.is_wall(self.x, new_y):
                self.y = new_y
