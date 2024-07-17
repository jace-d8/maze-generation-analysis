import pygame
from src import constants as c
from app import App


class Cell:
    def __init__(self, x, y):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.generated = False
        self.color = c.BLACK
        self.size = App.SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def generate(self):
        self.generated = True
        self.color = c.WHITE

    def draw(self):
        # Draw the cell rectangle
        pygame.draw.rect(App.SCREEN, self.color, (self.x, self.y, self.size, self.size))
        wall_color = c.BLACK if self.generated else c.WHITE
        # Draw the cell borders; if maze path impedes the cell from certain direction, that direction will not be drawn

        if self.walls["top"]:
            pygame.draw.line(App.SCREEN, wall_color, (self.x, self.y), (self.x + self.size, self.y), c.WALL_WIDTH)
        if self.walls["right"]:
            pygame.draw.line(App.SCREEN, wall_color, (self.x + self.size, self.y),
                             (self.x + self.size, self.y + self.size), c.WALL_WIDTH)
        if self.walls["bottom"]:
            pygame.draw.line(App.SCREEN, wall_color, (self.x, self.y + self.size),
                             (self.x + self.size, self.y + self.size), c.WALL_WIDTH)
        if self.walls["left"]:
            pygame.draw.line(App.SCREEN, wall_color, (self.x, self.y), (self.x, self.y + self.size), c.WALL_WIDTH)

    def update_size(self, new_size):
        self.size = new_size

    def update_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
