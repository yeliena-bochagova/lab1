import pytest
from map import Map
from tile import Tile

@pytest.fixture
def simple_map():
    """Фікстура: створює мапу 3x3"""
    return Map(3, 3)

def test_is_wall_within_bounds(simple_map):
    """Перевірка: клітинка не є стіною після створення"""
    assert simple_map.is_wall(1, 1) is False