import pygame
import sys
from player import Player
from ghost import Ghost
from level import Level

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
        self.running = True
        self.direction = None