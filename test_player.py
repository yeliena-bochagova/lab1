from player import Player
from coin import Coin

# Для тесту потрібна хоча б заглушка для Map
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_wall(self, x, y):
        # Умовно — вся карта без стін
        return False

def test_player_movement():
    game_map = Map(10, 10)
    player = Player(5, 5)

    player.move("left", game_map)
    assert player.x == 4 and player.y == 5

    coin = Coin(4, 5)
    assert player.collect_coin(coin) == True
    assert player.score == 1

if __name__ == "__main__":
    test_player_movement()
    print("✅ Тести пройдено!")
