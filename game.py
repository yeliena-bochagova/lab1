import pygame
import sys
from player import Player
from ghost import Ghost
from level import Level

TILE_SIZE = 60
TOP_MARGIN = 40  # Відступ для верхньої панелі (наприклад, з рахунком)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600 + TOP_MARGIN))
        pygame.display.set_caption("PacMan Clone")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.level.generate_level()
        self.player = Player(1, 1)
        self.ghost = Ghost(5, 5)
        self.ghost_move_counter = 0
        self.player_move_counter = 0  # Лічильник руху гравця
        self.running = True
        self.direction = None
        self.game_over = False  # Флаг завершення гри
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        while True:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            # Якщо гра завершилась – показуємо меню "Game Over"
            if self.game_over:
                self.show_game_over_menu()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Якщо ми знаходимося у стані гри, обробляємо керування
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.direction = "up"
                    elif event.key == pygame.K_DOWN:
                        self.direction = "down"
                    elif event.key == pygame.K_LEFT:
                        self.direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"

    def update(self):
        # Обмежуємо частоту руху гравця
        self.player_move_counter += 1
        if self.player_move_counter >= 10:  # Рух кожні 10 кадрів
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

        # Рух привида кожні 30 кадрів (~2 рази за секунду)
        self.ghost_move_counter += 1
        if self.ghost_move_counter >= 30:
            self.ghost.move_random(self.level.map)
            self.ghost_move_counter = 0

        # Перевірка збору монет
        for coin in self.level.coins:
            if not coin.collected:
                self.player.collect_coin(coin)

        # Перевірка колізії гравець—привид
        if self.player.x == self.ghost.x and self.player.y == self.ghost.y:
            self.game_over = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Верхня панель для рахунку (на всю ширину екрану)
        background_rect = pygame.Rect(0, 0, self.screen.get_width(), TOP_MARGIN)
        pygame.draw.rect(self.screen, (0, 0, 255), background_rect)
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        # Відцентруємо текст у верхній панелі
        text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, TOP_MARGIN // 2))
        self.screen.blit(score_text, text_rect)

        # Малювання мапи та ігрових елементів (з урахуванням зсуву TOP_MARGIN)
        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                if self.level.map.tiles[y][x].is_wall:
                    pygame.draw.rect(
                        self.screen, (100, 100, 100),
                        (x * TILE_SIZE, y * TILE_SIZE + TOP_MARGIN, TILE_SIZE, TILE_SIZE)
                    )

        for coin in self.level.coins:
            if not coin.collected:
                pygame.draw.circle(
                    self.screen, (255, 255, 0),
                    (coin.x * TILE_SIZE + TILE_SIZE // 2, coin.y * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN), 10
                )

        pygame.draw.rect(
            self.screen, (0, 255, 0),
            (self.player.x * TILE_SIZE, self.player.y * TILE_SIZE + TOP_MARGIN, TILE_SIZE, TILE_SIZE)
        )

        pygame.draw.rect(
            self.screen, (255, 0, 0),
            (self.ghost.x * TILE_SIZE, self.ghost.y * TILE_SIZE + TOP_MARGIN, TILE_SIZE, TILE_SIZE)
        )

        pygame.display.flip()

    def show_game_over_menu(self):
        # Використовуємо окремий шрифт для меню
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

            # Створюємо напівпрозорий оверлей для затемнення екрану
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Чорний з 200 альфа-каналом (напівпрозорий)
            self.screen.blit(overlay, (0, 0))

            # Створюємо меню-блок у центрі, де фон синій
            menu_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 128), menu_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 3)  # рамка меню

            # Рендеримо тексти
            game_over_text = menu_font.render("Game Over", True, (255, 255, 255))
            score_text = menu_font.render(f"Score: {self.player.score}", True, (255, 255, 255))
            prompt_text = menu_font.render("Replay? (Y/N)", True, (255, 255, 255))

            # Центруємо тексти в меню-блоці
            game_over_rect = game_over_text.get_rect(center=(self.screen.get_width()//2, 200))
            score_rect = score_text.get_rect(center=(self.screen.get_width()//2, 260))
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width()//2, 320))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(prompt_text, prompt_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def restart_game(self):
        # Перегенеруємо рівень та скидаємо позиції і лічильники,
        # а також прапорець game_over.
        self.level.generate_level()
        self.player = Player(1, 1)
        self.ghost = Ghost(5, 5)
        self.game_over = False
        self.player_move_counter = 0
        self.ghost_move_counter = 0
        self.direction = None

if __name__ == "__main__":
    game = Game()
    game.run()
