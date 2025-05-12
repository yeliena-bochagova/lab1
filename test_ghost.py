import pytest
from game import Ghost

@pytest.fixture
def ghost():
    return Ghost(x=5, y=5)

def test_ghost_move(ghost):
    """Перевірка, чи змінюється координата привида після виклику move."""
    initial_x, initial_y = ghost.x, ghost.y
    ghost.move()
    assert (ghost.x, ghost.y) != (initial_x, initial_y)
