import pygame
import constants as c
from wrapper import Wrapper


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(Wrapper.SCREEN, c.WHITE, (self.x, self.y, self.width, self.height))


class MazeControls:
    print("IN PROGRESS")
