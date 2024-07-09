import pygame
from app import App
from maze_controls import Button
from maze_controls import BackDrop
import constants as c
from sys import exit


class Game:

    def __init__(self):
        self.gen_button = Button(480, 600, 200, 50, "Generate", c.GREEN, c.RED, 40)
        self.maze_gen_box = Button(260, 300, 40, 40, "Test", c.WHITE, c.LIGHT_GREEN, 20)
        self.backtrack_box = Button(260, 375, 40, 40, None, c.WHITE, c.LIGHT_GREEN, 20)
        self.path_gen_box = Button(260, 450, 40, 40, None, c.WHITE, c.LIGHT_GREEN, 20)
        self.time_delay_box = Button(260, 525, 40, 40, None, c.WHITE, c.LIGHT_GREEN, 20)
        self.title = Button(380, 200, 400, 70, "Maze Generator", c.BLACK, c.BLACK, 40)
        self.backdrop_a = BackDrop(c.BLACK, 200, 200, 800, 500)
        self.backdrop_b = BackDrop(c.WHITE, 190, 190, 820, 520)

        self.stage = 1
        self.coordinates_clicked = []
        self.generated = self.is_delay = False
        self.highlight_backtracking = self.watch_generation = self.watch_path = True

    def run(self, maze):

        while True:
            App.SCREEN.fill(c.WHITE)
            maze.draw_maze()

            if not self.generated:
                self.draw_all()

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

    def execute_generation(self, event, maze):

        if self.gen_button.is_clicked(event) and self.stage == 1:
            maze.generate_maze(self.watch_generation)
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
                maze.solve_maze(*self.coordinates_clicked[0], *self.coordinates_clicked[1], self.highlight_backtracking, self.watch_path)
                self.coordinates_clicked.clear()

    def draw_all(self):
        self.backdrop_b.draw()
        self.backdrop_a.draw()
        self.gen_button.draw()
        self.backtrack_box.draw()
        self.maze_gen_box.draw()
        self.path_gen_box.draw()
        self.time_delay_box.draw()
        self.title.draw()

