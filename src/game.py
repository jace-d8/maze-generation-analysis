import pygame
from app import App
from maze_controls import MazeControls
from src.analysis import Analysis
from src import constants as c
from sys import exit


class Game:
    def __init__(self):
        # Analyze
        self.analysis = Analysis()
        self.controls = MazeControls()
        # Game state
        self.stage = 1
        self.coordinates_clicked = []
        self.generated = self.is_delay = False
        self.highlight_backtracking = self.watch_generation = self.watch_path = True

    def run(self, maze):

        while True:
            maze.draw_maze()

            if not self.generated:
                self.controls.draw_menu()
            else:
                self.controls.draw_analyze_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.analysis.run(maze)
                    pygame.quit()
                    exit()

                self.controls.slider.update(event)
                maze.update_size(App.SIZE)
                self.controls.slider_title.update(f"Cell Size: {App.SIZE}")
                # to update the size the maze must reinitialized with the newly sized cells
                self.handle_checkboxes(event)
                self.execute_generation(event, maze, self.analysis)
                self.analysis.update_data()
            pygame.display.update()

    def handle_checkboxes(self, event):
        if self.stage == 1:
            if self.controls.maze_gen_box.is_clicked(event):
                self.watch_generation = not self.watch_generation
            if self.controls.backtrack_box.is_clicked(event):
                self.highlight_backtracking = not self.highlight_backtracking
            if self.controls.path_gen_box.is_clicked(event):
                self.watch_path = not self.watch_path
            if self.controls.time_delay_box.is_clicked(event):
                App.DELAY = 2 if self.controls.time_delay_box.is_checked else 0
        # OPTIMIZE LATER ^^^

    def execute_generation(self, event, maze, analysis):
        if self.controls.gen_button.is_clicked(event) and self.stage == 1:
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
