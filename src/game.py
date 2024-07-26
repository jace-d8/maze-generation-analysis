import pygame
from app import App
from maze_controls import MazeControls
from src.analysis import Analysis
import matplotlib.pyplot as plt
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
        self.generated = self.is_delay = self.run_analysis = self.exit_analysis = False
        self.highlight_backtracking = self.watch_generation = self.watch_path = True

    def run(self, maze):

        while True:
            maze.draw_maze()

            if not self.generated:
                self.controls.draw_menu()
            elif self.run_analysis and not self.exit_analysis:
                if self.stage == 2:
                    self.analysis.run(maze)  # could add a count and have iterations for the count
                    self.stage = 3
                self.controls.entropy.update(f"Shannon's Entropy: {self.analysis.entropy:.3f}")
                self.controls.prob_distribution.update(f"{self.analysis.probability_distribution}")

                # TMP
                plt.figure(figsize=(4, 2))
                plt.plot([1, 2, (App.COLS * App.ROWS)], [1, 2, 3])  # x[0 to max entropy] y[0 to cell count]
                # print(maze.size)
                plt.title('Sample Plot')
                plt.savefig('plot.png', bbox_inches='tight', pad_inches=0.1)
                plt.close()
                img = pygame.image.load('plot.png')
                self.controls.draw_analyze_menu()
                App.SCREEN.blit(img, (220, 470))

            elif not self.exit_analysis:
                self.controls.analyze_button.draw()
                self.controls.analyze_title.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.handle_slider(event, maze)
                print(App.COLS * App.ROWS)
                self.execute_generation(event, maze, self.analysis)
                self.handle_buttons(event)

            pygame.display.update()

    def handle_slider(self, event, maze):
        self.controls.slider.update(event)
        maze.update_size(App.SIZE)
        self.controls.slider_title.update(f"Cell Size: {App.SIZE}")
        # to update the size the maze must reinitialized with the newly sized cells

    def handle_buttons(self, event):
        if self.stage == 1:
            if self.controls.maze_gen_box.is_clicked(event):
                self.watch_generation = not self.watch_generation
            if self.controls.backtrack_box.is_clicked(event):
                self.highlight_backtracking = not self.highlight_backtracking
            if self.controls.path_gen_box.is_clicked(event):
                self.watch_path = not self.watch_path
            if self.controls.time_delay_box.is_clicked(event):
                App.DELAY = 2 if self.controls.time_delay_box.is_checked else 0
        else:
            if self.controls.analyze_button.is_clicked(event):
                self.run_analysis = True
            if self.controls.exit_analysis.is_clicked(event):
                self.exit_analysis = True
        # OPTIMIZE LATER ^^^

    def execute_generation(self, event, maze, analysis):
        if self.controls.gen_button.is_clicked(event) and self.stage == 1:
            maze.generate_maze(self.watch_generation, analysis)
            maze.solve_maze(0, 0, App.COLS - 1, App.ROWS - 1, self.highlight_backtracking, self.watch_path)
            self.stage = 2
            self.generated = True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.stage != 1:
            # if the buttons are drawn, don't allow for them to be clicked through
            if self.run_analysis and not self.exit_analysis: # need another condition for analysis button
                if (not self.controls.analyze_button.rect.collidepoint(pygame.mouse.get_pos()) and
                        not any(item.rect.collidepoint(pygame.mouse.get_pos()) for item in self.controls.analyze_menu)):
                    self.handle_clicks(maze)
            else:
                self.handle_clicks(maze)

    def handle_clicks(self, maze):
        maze.reset_maze()
        x, y = (pos // App.SIZE for pos in pygame.mouse.get_pos())
        # pos is a tuple(x,y), pos is divided and floored
        maze.maze[x][y].color = c.LIGHT_RED
        self.coordinates_clicked.append((x, y))
        if len(self.coordinates_clicked) == 2:
            maze.solve_maze(*self.coordinates_clicked[0], *self.coordinates_clicked[1],
                            self.highlight_backtracking, self.watch_path)
            self.coordinates_clicked.clear()
