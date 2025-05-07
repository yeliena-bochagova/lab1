import pygame
from player import Player
from ghost import Ghost
from level import Level

TILE_SIZE = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("PacMan Clone")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.level.generate_level()
        self.player = Player(1, 1)
        self.ghost = Ghost(5, 5)
        self.ghost_move_counter = 0
        self.player_move_counter = 0  # Додаємо лічильник руху гравця
        self.running = True
        self.direction = None

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
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
        if self.player_move_counter >= 10:  # Рух кожні 10 кадрів (можна змінити це число)
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

        # Рух привида по 30 кадрів
        self.ghost_move_counter += 1
        if self.ghost_move_counter >= 30:  # Рух привида раз на 30 кадрів (~2 рази на секунду)
            self.ghost.move_random(self.level.map)
            self.ghost_move_counter = 0

        # Перевірка на збір монет
        for coin in self.level.coins:
            if not coin.collected:
                self.player.collect_coin(coin)

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Малювання мапи (стіни)
        for y in range(self.level.map.height):
            for x in range(self.level.map.width):
                if self.level.map.tiles[y][x].is_wall:
                    pygame.draw.rect(
                        self.screen, (56, 17, 173),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

        # Малювання монет
        for coin in self.level.coins:
            if not coin.collected:
                pygame.draw.circle(
                    self.screen, (255, 255, 0),
                    (coin.x * TILE_SIZE + TILE_SIZE // 2, coin.y * TILE_SIZE + TILE_SIZE // 2), 10
                )

        # Малювання гравця
        pygame.draw.rect(
            self.screen, (0, 255, 0),
            (self.player.x * TILE_SIZE, self.player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

        # Малювання привида
        pygame.draw.rect(
            self.screen, (255, 0, 0),
            (self.ghost.x * TILE_SIZE, self.ghost.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
