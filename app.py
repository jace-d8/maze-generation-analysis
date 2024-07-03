import pygame


class App:
    SCREEN = pygame.display.set_mode((1202, 802))
    SIZE = 50
    COLS = int(SCREEN.get_width() / SIZE)
    ROWS = int(SCREEN.get_height() / SIZE)
    DELAY = 1
