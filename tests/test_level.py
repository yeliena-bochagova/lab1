from level import Level

def test_generate_level_creates_coins():
    """Перевірка: після generate_level монети додано"""
    level = Level()
    level.generate_level()
    assert len(level.coins) > 0  # Має бути хоча б одна монета

def test_generate_level_has_some_walls():
    """Перевірка: хоча б одна клітинка має бути стіною"""
    level = Level()
    level.generate_level()
    wall_count = sum(tile.is_wall for row in level.map.tiles for tile in row)
    assert wall_count > 0