import pygame
SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 204, 0)
LIGHT_RED = (255, 153, 156)
SCREEN = pygame.display.set_mode((1202, 802))
# the dimensions must be divisible by the size - remainder of two so the borders( of width 2) can be seen
COLS = int(SCREEN.get_width() / SIZE)
ROWS = int(SCREEN.get_height() / SIZE)
WALL_WIDTH = 2
