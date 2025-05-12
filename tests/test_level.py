from level import Level

def test_generate_level_creates_coins():
    """Перевірка: після generate_level монети додано"""
    level = Level()
    level.generate_level()
    assert len(level.coins) > 0  # Має бути хоча б одна монета

