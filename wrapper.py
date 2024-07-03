import pygame


class Wrapper:
    def game_loop(self):
        print("IN PROGRESS")

    SCREEN = pygame.display.set_mode((1202, 802))
    SIZE = 8
    COLS = int(SCREEN.get_width() / SIZE)
    ROWS = int(SCREEN.get_height() / SIZE)
    DELAY = 1

