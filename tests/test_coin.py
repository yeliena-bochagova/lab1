import pytest
from coin import Coin

@pytest.fixture
def coin():
    """Фікстура для створення монети."""
    return Coin(2, 2)

def test_coin_disappears(coin):
    """Перевірка, що монета зникає при зборі."""
    coin.collected = False
    assert coin.collected is False

    coin.collected = True
    assert coin.collected is True
