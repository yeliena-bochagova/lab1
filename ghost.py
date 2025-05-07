import random

class Ghost:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        # Якщо потрібна ідея "швидкості", замість дробового значення
        # використовуйте логіку затримки руху (напр., в Game)
        self.speed = 1

    def move_random(self, map):
        """Випадковий рух привида по сітці."""
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)

        # Використовуємо дискретний рух: зміщення цілим числом 1
        new_x, new_y = self.x, self.y
        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1

        if not map.is_wall(new_x, new_y):
            self.x, self.y = new_x, new_y

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
