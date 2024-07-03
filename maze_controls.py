import pygame
import constants as c
from app import App


class Button:
    def __init__(self, x, y, w, h, text, color, hov_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hov_color
        self.font = pygame.font.SysFont('Arial', 40)
        self.is_checked = False

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(App.SCREEN, self.hover_color, self.rect)
        else:
            pygame.draw.rect(App.SCREEN, self.color, self.rect)

        text_surf = self.font.render(self.text, True, c.WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        App.SCREEN.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False


class MazeControls:
    print("IN PROGRESS")
