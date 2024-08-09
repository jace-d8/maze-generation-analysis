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
            self.manage_gui(maze)  # Deal with analyze button clicking !!!

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
            if self.run_analysis and not self.exit_analysis:  # need another condition for analysis button
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

    def manage_graphs(self):
        plt.figure(figsize=(4, 2))
        # plt.plot([1, 2, 4], [1, 2, 3])  # x[0 to max entropy] y[0 to cell count]
        values = list(self.analysis.total_direction_count.values())
        key = list(self.analysis.total_direction_count.keys())
        bars = plt.bar(key, values, color='red', edgecolor='black', linewidth=1.2, width=0.6)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        # Labels and title
        plt.xlabel('Directions', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.title('Total Direction Count', fontsize=14)
        # Adjust y-axis limits to better show differences
        plt.ylim(0, max(values) * 1.2)
        plt.savefig('plot.png', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        return pygame.image.load('../src/plot.png')

    def manage_gui(self, maze):
        # TMP
        if not self.generated:
            self.controls.draw_menu()
        elif self.run_analysis and not self.exit_analysis:
            if self.stage == 2:
                self.analysis.run(maze)  # could add a count and have iterations for the count
                self.stage = 3
            self.controls.entropy.update(f"Shannon's Entropy: {self.analysis.entropy:.3f}")
            self.controls.prob_distribution.update(f"{self.analysis.probability_distribution}")
            # TMP
            self.controls.draw_analyze_menu()
            img = self.manage_graphs()
            App.SCREEN.blit(img, (220, 400))  # Blit to specific coords
        elif not self.exit_analysis:
            self.controls.analyze_button.draw()
            self.controls.analyze_title.draw()
