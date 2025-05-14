import pytest
from ghost import Ghost
from unittest.mock import MagicMock

@pytest.fixture
def ghost():
    """Фікстура для створення привида."""
    return Ghost(3, 3)

def test_move_random(ghost):
    """Перевірка, чи змінюється координата після виклику move_random."""
    map_mock = MagicMock()
    map_mock.is_wall.return_value = False  # Мок стін
    ghosts = [ghost]

    old_x, old_y = ghost.x, ghost.y
    ghost.move_random(map_mock, ghosts)

    assert (ghost.x, ghost.y) != (old_x, old_y)
