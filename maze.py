import pygame
import pygame.rect
import constants as c
import random


class Cell:
    def __init__(self, x, y):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.generated = False
        self.color = c.BLACK
        self.size = c.SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def generate(self):
        self.generated = True
        self.color = c.WHITE

    def draw(self):
        # Draw the cell rectangle
        pygame.draw.rect(c.SCREEN, self.color, (self.x, self.y, self.size, self.size))
        wall_color = c.BLACK if self.generated else c.WHITE
        # Draw the cell borders; if maze path impedes the cell from certain direction, that direction will not be drawn

        if self.walls["top"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y), (self.x + self.size, self.y), c.WALL_WIDTH)
        if self.walls["right"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x + self.size, self.y),
                             (self.x + self.size, self.y + self.size), c.WALL_WIDTH)
        if self.walls["bottom"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y + self.size),
                             (self.x + self.size, self.y + self.size), c.WALL_WIDTH)
        if self.walls["left"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y), (self.x, self.y + self.size), c.WALL_WIDTH)


class Maze:
    def __init__(self):
        self.maze = [[Cell(i * c.SIZE, j * c.SIZE) for j in range(c.ROWS)] for i in range(c.COLS)]

    def generate_maze(self, maze_gen_box):
        self.gen_maze_helper(random.randint(0, c.COLS - 1), random.randint(0, c.ROWS - 1), maze_gen_box)
        # Pass in a random starting point for the maze to begin generation

    def gen_maze_helper(self, x, y, maze_gen_box):

        # check validity of current cell - if invalid return false
        if x + 1 > c.COLS or y + 1 > c.ROWS or x < 0 or y < 0 or self.maze[x][y].generated:
            return
        else:  # else this cell is valid can be updated to visited
            self.maze[x][y].generate()

            # draw maze for visuals
            if maze_gen_box:
                self.draw_maze()  # temp
                pygame.display.update()  # temp

        compass = [  # contains direction coords and label
            ((x, y - 1), "up"),
            ((x, y + 1), "down"),
            ((x + 1, y), "right"),
            ((x - 1, y), "left")
        ]
        # choose random direction, if the direction is invalid, remove it and try again
        for (newX, newY), direction in random.sample(compass, len(compass)):
            if 0 <= newX < c.COLS and 0 <= newY < c.ROWS and not self.maze[newX][newY].generated:
                if direction == "up":
                    self.maze[x][y].walls["top"] = False
                    self.maze[newX][newY].walls["bottom"] = False
                elif direction == "right":
                    self.maze[x][y].walls["right"] = False
                    self.maze[newX][newY].walls["left"] = False
                elif direction == "down":
                    self.maze[x][y].walls["bottom"] = False
                    self.maze[newX][newY].walls["top"] = False
                elif direction == "left":
                    self.maze[x][y].walls["left"] = False
                    self.maze[newX][newY].walls["right"] = False

            self.gen_maze_helper(newX, newY, maze_gen_box)  # recursive step. If backtracking will occur if-
            # there are more directions available in the loop

    def draw_maze(self):
        for i in range(c.COLS):
            for j in range(c.ROWS):
                self.maze[i][j].draw()
            #pygame.time.delay(c.DELAY)

    def reset_maze(self):
        for i in range(c.COLS):
            for j in range(c.ROWS):
                self.maze[i][j].color = c.WHITE

    def solve_maze(self, x, y, end_x, end_y, highlight_backtracking):
        current_cell = self.maze[x][y]  # for simplification
        current_cell.color = c.RED  # mark the cell visited by default

        self.draw_maze()  # temp
        pygame.display.update()  # temp

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
                    if self.solve_maze(*new_direction_coords, end_x, end_y, highlight_backtracking):
                        if current_cell.color == c.RED:
                            current_cell.color = c.GREEN
                            self.maze[end_x][end_y].color = c.GREEN
                        return True  # This will send "True" up the call stack and end the recursion

            current_cell.color = c.LIGHT_RED if highlight_backtracking else c.WHITE
            # we've hit a dead end and must backtrack, turn this cell white
            self.draw_maze()  # temp
            pygame.display.update()  # temp
            return False
        # if we return to start and all surrounding cells have been hit , maze has no exit (which should never happen)


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(c.SCREEN, c.WHITE, (self.x, self.y, self.width, self.height))
