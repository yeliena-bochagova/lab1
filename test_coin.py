import pytest
from game import Coin

@pytest.fixture
def coin():
    return Coin(x=3, y=3)

def test_coin_disappears_on_collect(coin):
    """Перевірка, що монета зникає після збору."""
    coin.collect()
    assert coin.is_collected is True
