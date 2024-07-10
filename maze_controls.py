import pygame
import constants as c
from app import App


class GUIRect:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self):
        pygame.draw.rect(App.SCREEN, self.color, self.rect)


class Button(GUIRect):
    def __init__(self, x, y, w, h, color, hov_color):
        super().__init__(x, y, w, h, color)
        self.hover_color = hov_color
        self.is_checked = False

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(App.SCREEN, self.hover_color, self.rect)
        else:
            super().draw()

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False


class TextBox(GUIRect):
    def __init__(self, x, y, w, h, color, text, font_size):
        super().__init__(x, y, w, h, color)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)

    def draw(self):
        text_surf = self.font.render(self.text, True, c.WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        App.SCREEN.blit(text_surf, text_rect)


class Slider:
    def __init__(self, button_color, slider_color, x, y, w, h):
        self.button_color = button_color
        self.slider_color = slider_color
        # self.button = pygame.Rect()
        self.slider = pygame.Rect(x, y, w, h)
