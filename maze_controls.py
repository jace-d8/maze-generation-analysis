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
        self.text = str(text)
        self.font = pygame.font.SysFont('Arial', font_size)

    def draw(self):
        text_surf = self.font.render(self.text, True, c.WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        App.SCREEN.blit(text_surf, text_rect)

    def update(self, text):
        self.text = str(text)


class Slider(GUIRect):
    def __init__(self, slider_x, slider_y, slider_width, slider_height, button_width, button_height, color, slider_color):
        self.slider_color = slider_color
        self.slider = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        self.button_x = self.slider.centerx - button_width / 2
        self.button_y = self.slider.centery - button_height / 2
        self.drag = False
        super().__init__(self.button_x, self.button_y, button_width, button_height, color)

    def draw(self):
        pygame.draw.rect(App.SCREEN, self.slider_color, self.slider, border_radius=20)
        super().draw()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.drag = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.drag = False
        if self.drag:
            if 600 >= pygame.mouse.get_pos()[1] >= 250:
                self.rect.y = pygame.mouse.get_pos()[1]
        slider_value = {
            range(575, 600): 4,
            range(550, 575): 5,
            range(525, 550): 8,
            range(500, 525): 10,
            range(475, 500): 16,
            range(450, 475): 20,
            range(425, 450): 25,
            range(400, 425): 40,
            range(375, 400): 50,
            range(350, 375): 80,
            range(325, 350): 100,
            range(275, 300): 200,
            range(250, 275): 400,
        }
        for mouse_range, value in slider_value.items():
            if self.rect.y in mouse_range:
                App.SIZE = value
                App.COLS = int(App.SCREEN.get_width() / App.SIZE)
                App.ROWS = int(App.SCREEN.get_height() / App.SIZE)
                break
