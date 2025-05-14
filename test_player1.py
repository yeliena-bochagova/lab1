import pytest
from unittest.mock import Mock
from game import Player, Coin  # Імпортуємо відповідні класи

@pytest.fixture
def player():
    return Player(x=0, y=0)

@pytest.fixture
def coin():
    return Coin(x=1, y=1)

@pytest.mark.parametrize("dx, dy", [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_player_move(player, dx, dy):
    """Перевірка переміщення гравця у різні напрямки."""
    initial_x, initial_y = player.x, player.y
    player.move(dx, dy)
    assert player.x == initial_x + dx
    assert player.y == initial_y + dy

def test_player_collect_coin(player, coin):
    """Перевірка збору монети."""
    player.x, player.y = coin.x, coin.y  # Гравець на позиції монети
    assert player.collect_coin(coin) is True  # Перевіряємо, що монета зібрана
    assert coin.collected is True  # Перевіряємо, що монета позначена як зібрана
