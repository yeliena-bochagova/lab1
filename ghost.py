import random

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        if abs(dx) > abs(dy):
            self.x += 1 if dx > 0 else -1
        else:
            self.y += 1 if dy > 0 else -1
