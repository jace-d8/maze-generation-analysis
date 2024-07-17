import pygame
import pygame.rect
from cell import Cell
from app import App
from src import constants as c
import random


class Maze:
    def __init__(self):
        self.maze = [[Cell(i * App.SIZE, j * App.SIZE) for j in range(App.ROWS)] for i in range(App.COLS)]

    def generate_maze(self, maze_gen_box, analysis):
        self.gen_maze_helper(random.randint(0, App.COLS - 1), random.randint(0, App.ROWS - 1), maze_gen_box, analysis)
        # Pass in a random starting point for the maze to begin generation

    def gen_maze_helper(self, x, y, maze_gen_box, analysis):
        # check validity of current cell - if invalid return false
        if x + 1 > App.COLS or y + 1 > App.ROWS or x < 0 or y < 0 or self.maze[x][y].generated:
            return
        else:  # else this cell is valid can be updated to visited
            self.maze[x][y].generate()

            if maze_gen_box:
                self.draw_maze()
                pygame.display.update()

        compass = [  # contains direction coords and label
            ((x, y - 1), "up"),
            ((x, y + 1), "down"),
            ((x + 1, y), "right"),
            ((x - 1, y), "left")
        ]

        self.gen_direction(compass, x, y, maze_gen_box, analysis)

    def gen_direction(self, compass, x, y, maze_gen_box, analysis):
        wall_updates = {
            "up": ("top", "bottom"),
            "right": ("right", "left"),
            "down": ("bottom", "top"),
            "left": ("left", "right")
        }
        # choose random direction, if the direction is invalid, remove it and try again
        for (newX, newY), direction in random.sample(compass, len(compass)):
            if 0 <= newX < App.COLS and 0 <= newY < App.ROWS and not self.maze[newX][newY].generated:
                analysis.directional_variation(direction)
                wall1, wall2 = wall_updates[direction]
                self.maze[x][y].walls[wall1] = False
                self.maze[newX][newY].walls[wall2] = False
            self.gen_maze_helper(newX, newY, maze_gen_box, analysis)  # recursive step. If backtracking will occur if-
            # there are more directions available in the loop

    def draw_maze(self):
        for i in range(App.COLS):
            for j in range(App.ROWS):
                self.maze[i][j].draw()
            pygame.time.delay(App.DELAY)

    def reset_maze(self):
        for i in range(App.COLS):
            for j in range(App.ROWS):
                self.maze[i][j].color = c.WHITE

    # returns maze to default color making it "unvisited"

    def update_size(self, new_size):
        for i in range(App.COLS):
            for j in range(App.ROWS):
                self.maze[i][j].update_size(new_size)
                self.maze[i][j].update_pos(i * new_size, j * new_size)

    # visits every cell in the maze to update the size according to the slider

    def solve_maze(self, x, y, end_x, end_y, highlight_backtracking, watch_path):
        current_cell = self.maze[x][y]  # for simplification
        current_cell.color = c.RED  # mark the cell visited by default

        if watch_path:
            self.draw_maze()
            pygame.display.update()

        compass = [  # the cell walls and the direction needed to move to next cell in said direction
            (current_cell.walls["top"], (x, y - 1)),
            (current_cell.walls["bottom"], (x, y + 1)),
            (current_cell.walls["right"], (x + 1, y)),
            (current_cell.walls["left"], (x - 1, y))
        ]
        if y == end_y and x == end_x:  # the location of the last cell
            return True  # return True if end location is reached
        else:
            # choose random direction, if the direction is invalid, remove it and try again
            # backtracking will happen by default if there are more directions available
            for wall, new_direction_coords in random.sample(compass, len(compass)):
                new_x, new_y = new_direction_coords
                if not wall and self.maze[new_x][new_y].color != c.RED:  # if wall is not present go that way
                    if self.solve_maze(*new_direction_coords, end_x, end_y, highlight_backtracking, watch_path):
                        if current_cell.color == c.RED:
                            current_cell.color = c.GREEN
                            self.maze[end_x][end_y].color = c.GREEN
                        return True  # This will send "True" up the call stack and end the recursion

            current_cell.color = c.LIGHT_RED if highlight_backtracking else c.WHITE
            # we've hit a dead end and must backtrack, turn this cell white
            if watch_path:
                self.draw_maze()
                pygame.display.update()
            return False
        # if we return to start and all surrounding cells have been hit , maze has no exit (which should never happen)
