import pygame
from src import constants as c
from app import App


# GET RID OF W AND H ON TEXT
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
        self.clicked_color = c.GREEN
        self.is_checked = False

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(App.SCREEN, self.hover_color, self.rect, border_radius=10)
        else:
            super().draw()

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.is_checked = not self.is_checked
                self.color = c.GREEN if self.is_checked else c.WHITE
                return True
        return False


class TextBox(GUIRect):
    def __init__(self, x, y, w, h, color, text, font_size):
        super().__init__(x, y, w, h, c.WHITE)
        self.text = str(text)
        self.color = color
        self.font = pygame.font.SysFont('Arial', font_size)

    def draw(self):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        App.SCREEN.blit(text_surf, text_rect)

    def update(self, text):
        self.text = str(text)


class Slider(GUIRect):
    def __init__(self, slider_x, slider_y, slider_width, slider_height, button_width, button_height, color,
                 slider_color):
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
            if self.rect.y in range(249, 601):
                self.rect.y = pygame.mouse.get_pos()[1]
                # Only update the sliders position if it is within the given Y bounds
            if self.rect.y < 250:
                self.rect.y = 250
            if self.rect.y > 600:
                self.rect.y = 600

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
            range(250, 275): 400,  # increased upper and lower bounds for smoother interaction
        }
        # A dictionary to correlate the y value of the slider and a given possible cell size
        for mouse_range, value in slider_value.items():
            if self.rect.y in mouse_range:
                App.SIZE = value
                App.COLS = int(App.SCREEN.get_width() / App.SIZE)
                App.ROWS = int(App.SCREEN.get_height() / App.SIZE)
                break


class MazeControls:
    def __init__(self):
        # Backdrops
        self.backdrop_b = GUIRect(190, 190, 820, 520, c.WHITE)
        self.backdrop_a = GUIRect(200, 200, 800, 500, c.BLACK)

        self.analysis_backdrop_b = GUIRect(190, 190, 820, 520, c.BLACK)
        self.analysis_backdrop_a = GUIRect(200, 200, 800, 500, c.WHITE)

        # Buttons
        self.gen_button = Button(480, 600, 200, 50, c.GREEN, c.RED)
        self.analyze_button = Button(1050, 25, 100, 50, c.LIGHT_BLACK, c.GREY)
        self.maze_gen_box = Button(260, 300, 40, 40, c.WHITE, c.LIGHT_GREEN)
        self.backtrack_box = Button(260, 375, 40, 40, c.WHITE, c.LIGHT_GREEN)
        self.path_gen_box = Button(260, 450, 40, 40, c.WHITE, c.LIGHT_GREEN)
        self.time_delay_box = Button(260, 525, 40, 40, c.WHITE, c.LIGHT_GREEN)

        # slider
        self.slider = Slider(860, 250, 40, 400, 50, 50, c.WHITE, c.GREY)

        # Textboxes
        self.gen_title = TextBox(480, 600, 200, 50, c.WHITE, "Generate", 40)
        self.analyze_title = TextBox(1000, 25, 200, 50, c.WHITE, "Analyze", 20)
        self.maze_gen_box_text = TextBox(380, 300, 40, 40, c.WHITE, "Skip maze animation", 20)
        self.backtrack_box_text = TextBox(420, 375, 40, 40, c.WHITE, "Turn off backtrack highlighting", 20)
        self.path_gen_box_text = TextBox(380, 450, 40, 40, c.WHITE, "Skip path generation", 20)
        self.time_delay_box_title = TextBox(380, 525, 40, 40, c.WHITE, "Slow-Mo generation", 20)
        self.title = TextBox(380, 200, 400, 70, c.BLACK, "Maze Generator", 40)
        self.slider_title = TextBox(750, 430, 40, 40, c.WHITE, f"Cell Size: {App.SIZE}", 20)
        self.entropy = TextBox(280, 220, 200, 50, c.BLACK, f"Shannon's Entropy: {0}", 30)
        self.prob_distribution = TextBox(280, 240, 200, 50, c.BLACK, f"{0}", 10)

        self.menu = [
            self.backdrop_b, self.backdrop_a, self.gen_button, self.maze_gen_box, self.backtrack_box, self.path_gen_box,
            self.time_delay_box, self.slider, self.gen_title, self.maze_gen_box_text, self.backtrack_box_text,
            self.path_gen_box_text, self.time_delay_box_title, self.title, self.slider_title
        ]
        self.analyze_menu = [
            self.analysis_backdrop_b, self.analysis_backdrop_a, self.entropy
        ]

    def draw_menu(self):
        for objects in self.menu:
            objects.draw()

    def draw_analyze_menu(self):
        for objects in self.analyze_menu:
            objects.draw()
