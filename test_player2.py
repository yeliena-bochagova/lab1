import pytest
from unittest.mock import MagicMock
from player import Player
from coin import Coin

@pytest.fixture
def player():
    """Фікстура для створення гравця."""
    return Player(5, 5)

@pytest.fixture
def coin():
    """Фікстура для створення монети."""
    return Coin(5, 5)

@pytest.mark.parametrize("direction, expected_x, expected_y", [
    ("up", 5, 4),
    ("down", 5, 6),
    ("left", 4, 5),
    ("right", 6, 5),
])
def test_move(player, direction, expected_x, expected_y):
    """Перевірка переміщення гравця."""
    map_mock = MagicMock()
    map_mock.is_wall.return_value = False  # Мок стін

    player.move(direction, map_mock)
    assert player.x == expected_x
    assert player.y == expected_y

def test_collect_coin(player, coin):
    """Перевірка збору монети."""
    assert player.collect_coin(coin) is True
    assert coin.collected is True
    assert player.score == 1
