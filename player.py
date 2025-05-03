from coin import Coin  
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0

    def move(self, direction):
        if direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        elif direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1

    def collect_coin(self, coin):
        if self.x == coin.x and self.y == coin.y and not coin.collected:
            coin.collected = True
            self.score += 1
