import pygame
from app import App
from maze_controls import Button
import constants as c
from sys import exit


class Game:

    def __init__(self):
        self.gen_button = Button(480, 600, 200, 50, "Generate", c.GREEN, c.RED)
        self.maze_gen_box = Button(260, 300, 40, 40, "A", c.GREEN, c.RED)
        self.backtrack_box = Button(260, 350, 40, 40, "B", c.GREEN, c.RED)
        self.path_gen_box = Button(260, 400, 40, 40, "C", c.GREEN, c.RED)

        self.stage = 1
        self.coordinates_clicked = []
        self.generated = self.is_delay = False
        self.highlight_backtracking = self.watch_generation = self.watch_path = True

    def run(self, maze):

        while True:
            App.SCREEN.fill(c.WHITE)
            maze.draw_maze()

            if not self.generated:
                self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_checkboxes(event)
                    self.execute_generation(event, maze)
            pygame.display.update()

    def handle_checkboxes(self, event):
        if self.stage == 1:
            if self.maze_gen_box.is_clicked(event):
                self.maze_gen_box.is_checked = not self.maze_gen_box.is_checked
                self.maze_gen_box.color = c.LIGHT_RED if self.maze_gen_box.is_checked else c.GREEN
                self.watch_generation = not self.watch_generation
            if self.backtrack_box.is_clicked(event):
                self.backtrack_box.is_checked = not self.backtrack_box.is_checked
                self.backtrack_box.color = c.LIGHT_RED if self.backtrack_box.is_checked else c.GREEN
                self.highlight_backtracking = not self.highlight_backtracking
            if self.path_gen_box.is_clicked(event):
                self.path_gen_box.is_checked = not self.path_gen_box.is_checked
                self.path_gen_box.color = c.LIGHT_RED if self.path_gen_box.is_checked else c.GREEN
                self.watch_path = not self.watch_path
        # OPTIMIZE LATER ^^^

    def execute_generation(self, event, maze):

        if self.gen_button.is_clicked(event) and self.stage == 1:
            maze.generate_maze(self.watch_generation)
            maze.solve_maze(0, 0, App.COLS - 1, App.ROWS - 1, self.highlight_backtracking)
            self.stage = 2
            self.generated = True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.stage == 2:
            maze.reset_maze()
            x, y = (pos // App.SIZE for pos in pygame.mouse.get_pos())
            # pos is a tuple(x,y), pos is divided and floored
            maze.maze[x][y].color = c.LIGHT_RED
            self.coordinates_clicked.append((x, y))
            if len(self.coordinates_clicked) == 2:
                maze.solve_maze(*self.coordinates_clicked[0], *self.coordinates_clicked[1], self.highlight_backtracking)
                self.coordinates_clicked.clear()

    def draw_buttons(self):
        self.gen_button.draw()
        self.backtrack_box.draw()
        self.maze_gen_box.draw()
        self.path_gen_box.draw()
        # size_slider.draw()
