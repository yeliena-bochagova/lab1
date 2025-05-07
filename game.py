import pygame
import sys
import random
from player import Player
from ghost import Ghost
from level import Level
from map import Map

TOP_MARGIN = 40  # Відступ для верхньої панелі (рахунок)


class Game:
    def __init__(self):
        pygame.init()
        # Створюємо вікно: ширина 600, висота 600 + TOP_MARGIN
        self.screen = pygame.display.set_mode((600, 600 + TOP_MARGIN))
        pygame.display.set_caption("PacMan Clone")
        self.clock = pygame.time.Clock()

        # Початкові налаштування: змінна "складність" гри
        self.tile_size = 60  # Збільшено з 30 до 60
        self.ghost_count = 3  # Початкова кількість привидів – 3

        # Створюємо рівень і перебудовуємо його відповідно до поточного tile_size.
        self.level = Level()  # Level конструктор без параметрів
        self.rebuild_level()  # За допомогою rebuild_level() замінюємо карту новою

        # Ініціалізуємо гравця і привидів
        self.player = Player(1, 1)
        self.ghosts = []
        self.init_ghosts()

        self.ghost_move_counter = 0
        self.player_move_counter = 0
        self.running = True
        self.game_over = False
        self.win = False  # Прапорець перемоги
        self.direction = None

        self.font = pygame.font.SysFont(None, 36)
        self.settings_open = False

    import random

    def init_ghosts(self):
        """
        Генерує привидів у випадкових координатах, перевіряючи, що вони:
        - Не стоять на стіні.
        - Не розташовані поруч один з одним (мінімальна відстань 2).
        """
        self.ghosts = []
        available_positions = []

        # Шукаємо всі прохідні клітинки
        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                if not self.level.map.is_wall(x, y):  # Клітинка має бути прохідною
                    available_positions.append((x, y))

        # Рандомно вибираємо позиції для привидів
        while len(self.ghosts) < self.ghost_count and available_positions:
            candidate = random.choice(available_positions)

            # Перевіряємо, чи новий привид знаходиться не надто близько до інших
            too_close = any(abs(candidate[0] - g.x) + abs(candidate[1] - g.y) < 2 for g in self.ghosts)

            if not too_close:
                self.ghosts.append(Ghost(candidate[0], candidate[1]))

            # Видаляємо використану позицію, щоб уникнути повторень
            available_positions.remove(candidate)

    def rebuild_level(self):
        """
        Перебудовує рівень, використовуючи поточне значення self.tile_size.
        Обчислює кількість клітинок за розмірами вікна, створює нову карту і викликає Level.generate_level().
        """
        new_width = self.screen.get_width() // self.tile_size
        new_height = (self.screen.get_height() - TOP_MARGIN) // self.tile_size
        self.level.map = Map(new_width, new_height)
        self.level.coins = []
        self.level.generate_level()

    def run(self):
        while True:
            self.handle_events()

            # Якщо гра активна і не у виграшному стані чи меню налаштувань – оновлюємо гру.
            if not self.game_over and not self.win and not self.settings_open:
                self.update()

            self.draw()

            # Якщо гравець програв – показуємо Game Over меню.
            if self.game_over:
                self.show_game_over_menu()
            # Якщо гравець виграв – показуємо меню виграшу.
            if self.win:
                self.show_win_menu()

            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_over and not self.win and not self.settings_open:
                    if event.key == pygame.K_q:
                        self.show_quit_menu()
                    elif event.key == pygame.K_s:
                        self.show_settings_menu()
                    elif event.key == pygame.K_UP:
                        self.direction = "up"
                    elif event.key == pygame.K_DOWN:
                        self.direction = "down"
                    elif event.key == pygame.K_LEFT:
                        self.direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"

    def update(self):
        # Рух гравця (кожні 10 кадрів)
        self.player_move_counter += 1
        if self.player_move_counter >= 10:
            if self.direction:
                new_x, new_y = self.player.x, self.player.y
                if self.direction == "up":
                    new_y -= 1
                elif self.direction == "down":
                    new_y += 1
                elif self.direction == "left":
                    new_x -= 1
                elif self.direction == "right":
                    new_x += 1
                if not self.level.map.is_wall(new_x, new_y):
                    self.player.move(self.direction, self.level.map)
            self.player_move_counter = 0

        # Рух кожного привида (кожні 30 кадрів)
        self.ghost_move_counter += 1
        if self.ghost_move_counter >= 30:
            for ghost in self.ghosts:
                ghost.move_random(self.level.map, self.ghosts)  # Додаємо self.ghosts
            self.ghost_move_counter = 0

        # Збирання монет
        for coin in self.level.coins:
            if not coin.collected:
                self.player.collect_coin(coin)

        # Перевірка зіткнення гравця з привидом
        for ghost in self.ghosts:
            if self.player.x == ghost.x and self.player.y == ghost.y:
                self.game_over = True
                break

        # Перевірка на перемогу: якщо всі монети зібрані, встановлюємо win.
        if self.level.coins and all(coin.collected for coin in self.level.coins):
            self.win = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Верхня панель з рахунком
        background_rect = pygame.Rect(0, 0, self.screen.get_width(), TOP_MARGIN)
        pygame.draw.rect(self.screen, (59, 37, 125), background_rect)
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, TOP_MARGIN // 2))
        self.screen.blit(score_text, text_rect)

        # Малювання карти: використання self.tile_size
        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                if self.level.map.tiles[y][x].is_wall:
                    pygame.draw.rect(
                        self.screen,
                        (59, 37, 125),
                        (x * self.tile_size, y * self.tile_size + TOP_MARGIN, self.tile_size, self.tile_size)
                    )

        # Малювання монет
        for coin in self.level.coins:
            if not coin.collected:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 0),
                    (coin.x * self.tile_size + self.tile_size // 2,
                     coin.y * self.tile_size + self.tile_size // 2 + TOP_MARGIN),
                    self.tile_size // 4
                )

        # Малювання гравця
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
            self.player.x * self.tile_size, self.player.y * self.tile_size + TOP_MARGIN, self.tile_size, self.tile_size)
        )

        # Малювання всіх привидів
        for ghost in self.ghosts:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (ghost.x * self.tile_size, ghost.y * self.tile_size + TOP_MARGIN, self.tile_size, self.tile_size)
            )

        pygame.display.flip()

    def show_quit_menu(self):
        menu_font = pygame.font.SysFont(None, 48)
        quit_menu_open = True

        while quit_menu_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        quit_menu_open = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_n:
                        quit_menu_open = False

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 128), menu_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)
            quit_text = menu_font.render("Quit Game?", True, (255, 255, 255))
            current_score = menu_font.render(f"Current Score: {self.player.score}", True, (255, 255, 255))
            prompt_text = menu_font.render("Quit? (Y/N)", True, (255, 255, 255))
            quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, 200))
            score_rect = current_score.get_rect(center=(self.screen.get_width() // 2, 260))
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 320))
            self.screen.blit(quit_text, quit_rect)
            self.screen.blit(current_score, score_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def show_game_over_menu(self):
        menu_font = pygame.font.SysFont(None, 48)
        menu_open = True

        while menu_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        menu_open = False
                        self.restart_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 128), menu_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)
            game_over_text = menu_font.render("Game Over", True, (255, 255, 255))
            final_score = menu_font.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
            prompt_text = menu_font.render("Restart? (Y/N)", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 200))
            score_rect = final_score.get_rect(center=(self.screen.get_width() // 2, 260))
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 320))
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score, score_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def show_settings_menu(self):
        """
        Меню налаштувань (складність): зміна tile_size через UP/DOWN та ghost_count через RIGHT/LEFT.
        Натискання Y зберігає зміни, після чого рівень перебудовується.
        Натискання N скасовує зміни.
        """
        settings_font = pygame.font.SysFont(None, 48)
        settings_open = True

        current_tile_size = self.tile_size
        current_ghost_count = self.ghost_count

        while settings_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_tile_size += 5
                    elif event.key == pygame.K_DOWN:
                        current_tile_size = max(10, current_tile_size - 5)
                    elif event.key == pygame.K_RIGHT:
                        current_ghost_count += 1
                    elif event.key == pygame.K_LEFT:
                        current_ghost_count = max(1, current_ghost_count - 1)
                    elif event.key == pygame.K_y:
                        self.tile_size = current_tile_size
                        self.ghost_count = current_ghost_count
                        settings_open = False
                        self.rebuild_level()
                        self.restart_game_partials()
                    elif event.key == pygame.K_n:
                        settings_open = False

            # Малюємо напівпрозорий фон меню
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            # Відмальовуємо прямокутник меню
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 128), menu_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)

            # Рендеримо кожен рядок окремо
            line1 = settings_font.render("Difficulty Settings", True, (255, 255, 255))
            line2 = settings_font.render(f"Tile Size: {current_tile_size}", True, (255, 255, 255))
            line3 = settings_font.render(f"Ghost Count: {current_ghost_count}", True, (255, 255, 255))
            line4 = settings_font.render("UP/DOWN: Tile", True, (255, 255, 255))
            line5 = settings_font.render("LEFT/RIGHT: Ghosts", True, (255, 255, 255))
            line6 = settings_font.render("Save: Y    Cancel: N", True, (255, 255, 255))

            # Обираємо координати, щоб розташувати рядки всередині меню
            center_x = self.screen.get_width() // 2
            # Ми розташовуємо рядки у меню між y = 170 та y = 430 (в межах прямокутника меню)
            line1_rect = line1.get_rect(center=(center_x, 170))
            line2_rect = line2.get_rect(center=(center_x, 220))
            line3_rect = line3.get_rect(center=(center_x, 270))
            line4_rect = line4.get_rect(center=(center_x, 320))
            line5_rect = line5.get_rect(center=(center_x, 370))
            line6_rect = line6.get_rect(center=(center_x, 420))

            self.screen.blit(line1, line1_rect)
            self.screen.blit(line2, line2_rect)
            self.screen.blit(line3, line3_rect)
            self.screen.blit(line4, line4_rect)
            self.screen.blit(line5, line5_rect)
            self.screen.blit(line6, line6_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def restart_game_partials(self):
        """
        Перезапускаємо гру, скинувши позиції гравця та привидів, але залишаємо рахунок.
        Перебудовуємо рівень за новими параметрами.
        """
        self.rebuild_level()
        self.player = Player(1, 1)
        self.init_ghosts()
        self.game_over = False
        self.win = False
        self.player_move_counter = 0
        self.ghost_move_counter = 0
        self.direction = None

    def restart_game(self):
        """
        Повний перезапуск гри після поразки: скидання рівня, позицій та (за бажанням) рахунку.
        Складність залишається незмінною.
        """
        self.rebuild_level()
        self.player = Player(1, 1)
        self.init_ghosts()
        self.game_over = False
        self.win = False
        self.player_move_counter = 0
        self.ghost_move_counter = 0
        self.direction = None
        # Якщо хочете скидати рахунок, додайте тут: self.player.score = 0

    def show_win_menu(self):
        """
        Меню, яке з’являється, коли гравець зібрав усі монети:
        "You Win!", відображення рахунку та запит "Try again? (Y/N)".
        Якщо Y – гра перезапускається, якщо N – гра завершується.
        """
        menu_font = pygame.font.SysFont(None, 48)
        win_menu_open = True

        while win_menu_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        win_menu_open = False
                        self.restart_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 128, 0), menu_rect)  # Зелений фон для перемоги
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)
            win_text = menu_font.render("You Win!", True, (255, 255, 255))
            score_text = menu_font.render(f"Score: {self.player.score}", True, (255, 255, 255))
            prompt_text = menu_font.render("Try again? (Y/N)", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(self.screen.get_width() // 2, 200))
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 260))
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 320))
            self.screen.blit(win_text, win_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    game = Game()
    game.run()
