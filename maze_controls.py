import pygame
import constants as c
from wrapper import Wrapper


class Button:
    def __init__(self, x, y, w, h, text, color, hov_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hov_color
        self.text = pygame.font.SysFont('Times New Roman', 40)

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(Wrapper.SCREEN, self.hover_color, self.rect)
            # Wrapper.SCREEN.blit(self.text)
        else:
            pygame.draw.rect(Wrapper.SCREEN, self.color, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False


class MazeControls:
    print("IN PROGRESS")
