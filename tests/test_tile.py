from tile import Tile

def test_tile_default():
    """Перевірка: за замовчуванням Tile не є стіною"""
    tile = Tile()
    assert tile.is_wall is False

def test_tile_with_wall():
    """Перевірка: Tile створюється як стіна, якщо is_wall=True"""
    tile = Tile(is_wall=True)
    assert tile.is_wall is True