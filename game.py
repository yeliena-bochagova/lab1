import pygame
import sys
import random
from player import Player
from ghost import Ghost
from level import Level  # Level() – конструктор без додаткових параметрів
from map import Map  # Map(width, height) створює карту потрібного розміру

TOP_MARGIN = 40  # Відступ для верхньої панелі (рахунок)


class Game:
    def __init__(self):
        pygame.init()
        # Створюємо вікно: ширина 600, висота 600 + TOP_MARGIN
        self.screen = pygame.display.set_mode((600, 600 + TOP_MARGIN))
        pygame.display.set_caption("PacMan Clone")
        self.clock = pygame.time.Clock()

        # Початкові налаштування
        self.tile_size = 60  # Чим менший tile_size, тим більше клітинок у рівні
        self.ghost_count = 1  # Початкова кількість привидів

        self.level = Level()  # Level конструктор без параметрів
        self.rebuild_level()  # Побудова рівня за поточними налаштуваннями

        self.player = Player(1, 1)
        self.ghosts = []
        self.init_ghosts()

        self.ghost_move_counter = 0
        self.player_move_counter = 0  # Лічильник руху гравця
        self.running = True  # Головний цикл гри
        self.game_over = False  # Прапорець завершення гри
        self.direction = None

        self.font = pygame.font.SysFont(None, 36)
        self.settings_open = False

    def init_ghosts(self):
        # Створюємо список привидів за кількістю ghost_count
        self.ghosts = []
        for i in range(self.ghost_count):
            self.ghosts.append(Ghost(5 + i, 5))

    def rebuild_level(self):
        """
        Перебудовує рівень, використовуючи поточне значення self.tile_size.
        Обчислює кількість клітинок у сітці на основі розмірів вікна.
        Заміщує self.level.map новою картою, і скидає self.level.coins.
        Потім викликає Level.generate_level() для заповнення лабіринту.
        """
        new_width = self.screen.get_width() // self.tile_size
        new_height = (self.screen.get_height() - TOP_MARGIN) // self.tile_size
        # Створюємо нову карту з заданою сіткою
        self.level.map = Map(new_width, new_height)
        # Очищаємо список монет
        self.level.coins = []
        # Генеруємо рівень (лабіринт і монети)
        self.level.generate_level()

    def run(self):
        while True:
            self.handle_events()
            if not self.game_over and not self.settings_open:
                self.update()
            self.draw()

            if self.game_over:
                self.show_game_over_menu()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_over and not self.settings_open:
                    if event.key == pygame.K_q:
                        self.show_quit_menu()
                    elif event.key == pygame.K_s:
                        self.show_settings_menu()  # Відкриваємо меню налаштувань
                    elif event.key == pygame.K_UP:
                        self.direction = "up"
                    elif event.key == pygame.K_DOWN:
                        self.direction = "down"
                    elif event.key == pygame.K_LEFT:
                        self.direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"

    def update(self):
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

        self.ghost_move_counter += 1
        if self.ghost_move_counter >= 30:
            for ghost in self.ghosts:
                ghost.move_random(self.level.map)
            self.ghost_move_counter = 0

        for coin in self.level.coins:
            if not coin.collected:
                self.player.collect_coin(coin)

        for ghost in self.ghosts:
            if self.player.x == ghost.x and self.player.y == ghost.y:
                self.game_over = True
                break

    def draw(self):
        self.screen.fill((0, 0, 0))
        background_rect = pygame.Rect(0, 0, self.screen.get_width(), TOP_MARGIN)
        pygame.draw.rect(self.screen, (0, 0, 255), background_rect)
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, TOP_MARGIN // 2))
        self.screen.blit(score_text, text_rect)

        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                if self.level.map.tiles[y][x].is_wall:
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 100),
                        (x * self.tile_size, y * self.tile_size + TOP_MARGIN, self.tile_size, self.tile_size)
                    )

        for coin in self.level.coins:
            if not coin.collected:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 0),
                    (coin.x * self.tile_size + self.tile_size // 2,
                     coin.y * self.tile_size + self.tile_size // 2 + TOP_MARGIN),
                    self.tile_size // 4
                )

        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (self.player.x * self.tile_size, self.player.y * self.tile_size + TOP_MARGIN,
             self.tile_size, self.tile_size)
        )

        for ghost in self.ghosts:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (ghost.x * self.tile_size, ghost.y * self.tile_size + TOP_MARGIN,
                 self.tile_size, self.tile_size)
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
        Меню налаштувань (складність): зміна tile_size ("складність") через стрілки.
        При збереженні (Y) рівень перебудовується так, щоб заповнювати весь простір.
        Натискання N відміняє зміни.
        """
        settings_font = pygame.font.SysFont(None, 48)
        settings_open = True

        # Зберігаємо поточне значення tile_size для редагування
        current_tile_size = self.tile_size

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
                    elif event.key == pygame.K_y:
                        # Зберігаємо нове значення
                        self.tile_size = current_tile_size
                        settings_open = False
                        # Перебудовуємо рівень за новим tile_size
                        self.rebuild_level()
                        self.restart_game_partials()
                    elif event.key == pygame.K_n:
                        settings_open = False

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 128), menu_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)
            title_text = settings_font.render("Difficulty Settings", True, (255, 255, 255))
            tile_text = settings_font.render(f"Tile Size: {current_tile_size}", True, (255, 255, 255))
            prompt_text = settings_font.render("Adjust: UP/DOWN, Save: Y, Cancel: N", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 200))
            tile_rect = tile_text.get_rect(center=(self.screen.get_width() // 2, 260))
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 320))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(tile_text, tile_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def restart_game_partials(self):
        """
        Перезапускаємо гру частково (тобто скидаємо позиції гравця/привидів, але залишаємо рахунок).
        Після зміни налаштувань рівень перебудовується за новими параметрами.
        """
        self.rebuild_level()
        self.player = Player(1, 1)
        self.init_ghosts()
        self.game_over = False
        self.player_move_counter = 0
        self.ghost_move_counter = 0
        self.direction = None

    def restart_game(self):
        """
        Повний перезапуск гри після поразки: рівень, позиції та рахунок можна скидати,
        або залишати складність поточною.
        """
        self.rebuild_level()
        self.player = Player(1, 1)
        self.init_ghosts()
        self.game_over = False
        self.player_move_counter = 0
        self.ghost_move_counter = 0
        self.direction = None
        # Якщо бажаєте скидати рахунок, додайте тут self.player.score = 0


if __name__ == "__main__":
    game = Game()
    game.run()
