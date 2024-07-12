import pygame
import constants as c
from app import App


class GUIRect:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self):
        pygame.draw.rect(App.SCREEN, self.color, self.rect, border_radius=10)


class Button(GUIRect):
    def __init__(self, x, y, w, h, color, hov_color):
        super().__init__(x, y, w, h, color)
        self.hover_color = hov_color
        self.is_checked = False

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(App.SCREEN, self.hover_color, self.rect, border_radius=10)
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


class Slider(GUIRect):
    def __init__(self, slider_x, slider_y, slider_width, slider_height, button_width, button_height, color, slider_color):
        self.slider_color = slider_color
        self.slider = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        button_x = self.slider.centerx - button_width / 2
        super().__init__(button_x, self.slider.centery, button_width, button_height, color)

    def draw(self):
        pygame.draw.rect(App.SCREEN, self.slider_color, self.slider, border_radius=20)
        super().draw()

