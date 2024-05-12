import pygame
import constants as c
import random


class Cell:
    def __init__(self, x, y):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.visited = False
        self.size = c.SIZE
        self.direction = "none"

    def draw(self, screen):
        # Draw the cell rectangle
        if not self.visited:
            pygame.draw.rect(screen, c.WHITE, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(screen, c.RED, (self.x, self.y, self.size, self.size))
        # Draw the cell borders
        if self.direction != "down":
            pygame.draw.line(screen, c.BLACK, (self.x, self.y),
                             (self.x + self.size, self.y))  # top

        if self.direction != "right":
            pygame.draw.line(screen, c.BLACK, (self.x, self.y),
                             (self.x, self.y + self.size))  # left side

        if self.direction != "left":
            pygame.draw.line(screen, c.BLACK, (self.x + self.size, self.y),
                             (self.x + self.size, self.y + self.size))  # right side

        if self.direction != "up":
            pygame.draw.line(screen, c.BLACK, (self.x, self.y + self.size),
                             (self.x + self.size, self.y + self.size))  # bottom


# the problem may be because cells share borders - does that explain why right and down work tho?

class Maze:
    def __init__(self, cols, rows):
        self.maze = [[Cell(i * c.SIZE, j * c.SIZE) for j in range(rows)] for i in range(cols)]

    def generate_maze(self):
        x = random.randint(0, c.COLS - 1)
        y = random.randint(0, c.ROWS - 1)
        self.gen_maze_helper(x, y, "none")

    def gen_maze_helper(self, x, y, direction):
        valid_direction = False
        # check validity of current cell - if invalid return false
        if x + 1 > c.COLS or y + 1 > c.ROWS or x < 0 or y < 0 or self.maze[x][y].visited:
            return False
        else:  # else this cell is valid can be updated to visited
            self.maze[x][y].visited = True
            self.maze[x][y].direction = direction  # the direction taken to arrive at this cell
            # draw maze for visuals
            self.draw_maze(c.SCREEN, c.COLS, c.ROWS, False)  # temp
            pygame.display.update()  # temp
        while True:
            compass = [
                ((x, y + 1), "down"),
                ((x, y - 1), "up"),
                ((x + 1, y), "right"),
                ((x - 1, y), "left")
            ]
            for opt, direct in random.sample(compass, len(compass)):
                if self.gen_maze_helper(*opt, direct):  # try all directions at random until a valid one is found\
                    valid_direction = True
                    break
            if not valid_direction:
                break
        self.gen_maze_helper(*opt, direct)  # -- backtrack

    def draw_maze(self, screen, cols, rows, done):
        for i in range(cols):
            for j in range(rows):
                self.maze[i][j].draw(screen)
            if not done:
                pygame.time.delay(25)
                pygame.display.update()

        # this is for the original "animation" - it can be done every cell but gets too slow if there are 100+ cells

        """
        The Maze -
        The maze will be a graph of set vertices, the walls will be the 
        edges connecting the vertices, the randomization of edges will be done via some
        Algorithm
        Solving -
        Should be the easier part of the program; will use recursion or a stack and store each path taken
        in an array to display later
        Graphics - 
        The hard part
        """
