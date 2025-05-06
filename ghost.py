import random

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.8  # Трохи повільніше за гравця

    def move_random(self, map):
        """Випадковий рух привида."""
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)

        new_x, new_y = self.x, self.y
        if direction == "up":
            new_y -= self.speed
        elif direction == "down":
            new_y += self.speed
        elif direction == "left":
            new_x -= self.speed
        elif direction == "right":
            new_x += self.speed

        if not map.is_wall(new_x, new_y):
            self.x, self.y = new_x, new_y

    def chase_player(self, player, map):
        """Привид рухається до гравця (простий алгоритм)."""
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
