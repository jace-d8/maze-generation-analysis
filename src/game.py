import pygame
from app import App
from maze_controls import Button
from maze_controls import GUIRect
from maze_controls import TextBox
from maze_controls import Slider
from src.analysis import Analysis
from src import constants as c
from sys import exit


class Game:
    def __init__(self):
        # Analyze
        self.analysis = Analysis()
        # Backdrops
        self.backdrop_a = GUIRect(200, 200, 800, 500, c.BLACK)
        self.backdrop_b = GUIRect(190, 190, 820, 520, c.WHITE)

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

        # Game state
        self.stage = 1
        self.coordinates_clicked = []
        self.generated = self.is_delay = False
        self.highlight_backtracking = self.watch_generation = self.watch_path = True

    def run(self, maze):

        while True:
            maze.draw_maze()

            if not self.generated:
                self.draw_all()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.analysis.run(maze)
                    pygame.quit()
                    exit()

                self.slider.update(event)
                maze.update_size(App.SIZE)
                self.slider_title.update(f"Cell Size: {App.SIZE}")
                # to update the size the maze must reinitialized with the newly sized cells
                self.handle_checkboxes(event)
                self.execute_generation(event, maze, self.analysis)
                self.analysis.update_data()
            pygame.display.update()

    def handle_checkboxes(self, event):
        if self.stage == 1:
            if self.maze_gen_box.is_clicked(event):
                self.maze_gen_box.is_checked = not self.maze_gen_box.is_checked
                self.maze_gen_box.color = c.GREEN if self.maze_gen_box.is_checked else c.WHITE
                self.watch_generation = not self.watch_generation
            if self.backtrack_box.is_clicked(event):
                self.backtrack_box.is_checked = not self.backtrack_box.is_checked
                self.backtrack_box.color = c.GREEN if self.backtrack_box.is_checked else c.WHITE
                self.highlight_backtracking = not self.highlight_backtracking
            if self.path_gen_box.is_clicked(event):
                self.path_gen_box.is_checked = not self.path_gen_box.is_checked
                self.path_gen_box.color = c.GREEN if self.path_gen_box.is_checked else c.WHITE
                self.watch_path = not self.watch_path
            if self.time_delay_box.is_clicked(event):
                self.time_delay_box.is_checked = not self.time_delay_box.is_checked
                self.time_delay_box.color = c.GREEN if self.time_delay_box.is_checked else c.WHITE
                App.DELAY = 2 if self.time_delay_box.is_checked else 0
        # OPTIMIZE LATER ^^^

    def execute_generation(self, event, maze, analysis):
        if self.gen_button.is_clicked(event) and self.stage == 1:
            maze.generate_maze(self.watch_generation, analysis)
            maze.solve_maze(0, 0, App.COLS - 1, App.ROWS - 1, self.highlight_backtracking, self.watch_path)
            self.stage = 2
            self.generated = True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.stage == 2:
            maze.reset_maze()
            x, y = (pos // App.SIZE for pos in pygame.mouse.get_pos())
            # pos is a tuple(x,y), pos is divided and floored
            maze.maze[x][y].color = c.LIGHT_RED
            self.coordinates_clicked.append((x, y))
            if len(self.coordinates_clicked) == 2:
                maze.solve_maze(*self.coordinates_clicked[0], *self.coordinates_clicked[1], self.highlight_backtracking,
                                self.watch_path)
                self.coordinates_clicked.clear()

    def draw_all(self):
        draw_list = [
            self.backdrop_b, self.backdrop_a, self.gen_button, self.backtrack_box, self.maze_gen_box, self.path_gen_box,
            self.time_delay_box, self.title, self.gen_title, self.maze_gen_box_text, self.backtrack_box_text,
            self.path_gen_box_text, self.time_delay_box_title, self.slider, self.slider_title, self.analyze_button,
            self.analyze_title]
        # a list of drawable items
        for items in draw_list:
            items.draw()
