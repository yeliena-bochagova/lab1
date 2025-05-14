import pytest
import pygame
import sys
from unittest.mock import patch
from game import Game

# =======================
# ФІКСТУРА: Створюємо екземпляр гри для тестів.
# =======================
@pytest.fixture
def game_instance():
    """
    Фікстура, яка створює новий екземпляр Game.
    Для тестування руху ми змусимо оновлення відбуватися одразу,
    встановивши лічильники переміщення на порогові значення.
    """
    game = Game()
    # Щоб перевірка руху відбулася, встановимо лічильники
    game.player_move_counter = 10
    game.ghost_move_counter = 30
    return game

# =======================
# Тест генерації привидів: перевіряємо, що кількість привидів відповідає ghost_count
# та що між кожною парою привидів мінімум 1 вільний блок (Manhattan-відстань ≥ 2).
# =======================
def test_ghosts_initialized(game_instance):
    ghosts = game_instance.ghosts
    assert len(ghosts) == game_instance.ghost_count, "Кількість привидів не відповідає налаштуванням"
    for i in range(len(ghosts)):
        for j in range(i+1, len(ghosts)):
            distance = abs(ghosts[i].x - ghosts[j].x) + abs(ghosts[i].y - ghosts[j].y)
            assert distance >= 2, f"Привиди занадто близько один до одного: відстань {distance}"

# =======================
# Тест функції rebuild_level – перевіряємо, що після перебудови розміри карти змінюються.
# =======================
def test_rebuild_level(game_instance):
    old_width = game_instance.level.map.width
    old_height = game_instance.level.map.height
    # змінюємо tile_size і перебудовуємо рівень
    game_instance.tile_size += 10
    game_instance.rebuild_level()
    new_width = game_instance.level.map.width
    new_height = game_instance.level.map.height
    # Очікуємо, що розміри карти зміняться
    assert (new_width != old_width) or (new_height != old_height), "Розміри карти не змінилися після перебудови"

# =======================
# МОКУВАННЯ: Тест завершення гри.
# Підміняємо sys.exit та pygame.quit, щоб перевірити, чи викликали їх при події QUIT.
# =======================
@patch("sys.exit")
@patch("pygame.quit")
def test_quit_game(mock_quit, mock_exit, game_instance):
    # Надсилаємо QUIT-подію
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    # Встановлюємо running у True, щоб перевірити його зміну
    game_instance.running = True
    try:
        game_instance.handle_events()
    except SystemExit:
        pass
    # Перевіряємо, що running стає False і pygame.quit викликається
    assert game_instance.running is False, "running не змінено на False при QUIT-події"
    assert mock_quit.called, "pygame.quit не був викликаний при QUIT-події"
    # Якщо ви не очікуєте виклику sys.exit(), можна не перевіряти mock_exit

def test_initial_state(game_instance):
    # Перевіряємо, що атрибути ініціалізовано правильно
    assert game_instance.tile_size == 60
    assert game_instance.ghost_count == 3
    assert game_instance.running is True
    assert game_instance.game_over is False
    assert game_instance.win is False
    # Переконуємося, що екземпляри рівня, гравця та привидів створено
    assert game_instance.level is not None
    assert game_instance.player is not None
    # Перевірка кількості привидів (init_ghosts вже має запуститися у конструкторі чи виклику init_ghosts)
    assert len(game_instance.ghosts) <= game_instance.ghost_count
def test_draw_does_not_crash(game_instance):
    # Можна просто викликати draw() і перевірити, що не виникає помилок,
    # якщо метод нічого не повертає.
    try:
        game_instance.draw()
    except Exception as e:
        pytest.fail(f"Виклик draw() спричинив помилку: {e}")

@patch("sys.exit", side_effect=lambda: None)
@patch("pygame.quit")
def test_show_quit_menu(mock_quit, mock_exit, game_instance):
    # Моделюємо події: для прикладу, натискання Y (quit)
    quit_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y)
    # Створюємо подію QUIT для закриття циклу
    quit_events = [quit_event]

    # Патчимо pygame.event.get(), щоб повертати заданий список подій
    with patch("pygame.event.get", return_value=quit_events):
        try:
            game_instance.show_quit_menu()
        except SystemExit:
            pass
    # Перевіримо, що викликались функції завершення роботи
    assert mock_quit.called, "pygame.quit не був викликаний у show_quit_menu"
    assert mock_exit.called, "sys.exit не був викликаний у show_quit_menu"


def test_restart_game_partials(game_instance):
    # Змінюємо позицію гравця та привидів
    game_instance.player.x = 5
    game_instance.player.y = 5
    if game_instance.ghosts:
        game_instance.ghosts[0].x = 10

    game_instance.restart_game_partials()
    # Перевіряємо, що позиції скинулися. Залежно від логіки, ви можете порівняти з початковими значеннями.
    assert game_instance.player.x == 1, "Позиція гравця не скинута після restart_game_partials"
    assert game_instance.player.y == 1, "Позиція гравця не скинута після restart_game_partials"
    # Можна також перевірити, що рівень було перебудовано
    # (наприклад, шляхом зміни розмірів чи змісту карти)


def test_restart_game(game_instance):
    # Для повного перезапуску може знадобитися перевірити ігровий стан
    old_score = game_instance.player.score
    game_instance.restart_game()
    # Перевірити, що рівень перезавантажено, гри не закінчено тощо
    assert game_instance.game_over is False, "Після restart_game прапор game_over має бути False"
    # Якщо логіка передбачає скидання рахунку, перевірте це відповідно.

@pytest.mark.slow
def test_game_loop_execution(game_instance):
    # Патчимо методи меню, щоб уникнути виклику sys.exit()
    game_instance.show_game_over_menu = lambda: None
    game_instance.show_win_menu = lambda: None

    # Використовуємо фейкову реалізацію handle_events, щоб зупинити цикл
    count = 0
    def fake_handle_events():
        nonlocal count
        count += 1
        if count > 3:  # після 3 ітерацій зупиняємо гру
            game_instance.running = False
    game_instance.handle_events = fake_handle_events

    game_instance.run()  # Тепер цикл завершиться, коли running стане False
    assert count > 0, "Основний цикл ігри не виконувався"





