from tile import Tile

def test_tile_default():
    """Перевірка: за замовчуванням Tile не є стіною"""
    tile = Tile()
    assert tile.is_wall is False
