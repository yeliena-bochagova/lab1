class Player:
    def __init__(self, x, y):
        self.x = x  # Початкова позиція X
        self.y = y  # Початкова позиція Y
        self.score = 0  # Очки
        self.speed = 1  # Швидкість (1 клітинка за крок)

    def move(self, direction, map):
        """Рух гравця з перевіркою стін."""
        new_x, new_y = self.x, self.y

        if direction == "up":
            new_y -= self.speed
        elif direction == "down":
            new_y += self.speed
        elif direction == "left":
            new_x -= self.speed
        elif direction == "right":
            new_x += self.speed

        # Перевірка, чи нові координати не в стіні
        if not map.is_wall(new_x, new_y):
            self.x, self.y = new_x, new_y

    def collect_coin(self, coin):
        """Збір монети, якщо гравець на ній."""
        if self.x == coin.x and self.y == coin.y and not coin.collected:
            coin.collected = True
            self.score += 1
            return True
        return False
