import pygame
import constants as c
import random


class Cell:
    def __init__(self, x, y, visited):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.visited = False
        self.size = c.SIZE

    def draw(self, screen):
        # Draw the cell rectangle
        if not self.visited:
            pygame.draw.rect(screen, c.WHITE, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(screen, c.RED, (self.x, self.y, self.size, self.size))
        # Draw the cell borders
        pygame.draw.line(screen, c.BLACK, (self.x, self.y),
                         (self.x + self.size, self.y))  # top
        pygame.draw.line(screen, c.BLACK, (self.x, self.y),
                         (self.x, self.y + self.size))  # left side
        pygame.draw.line(screen, c.BLACK, (self.x + self.size, self.y),
                         (self.x + self.size, self.y + self.size))  # right side
        pygame.draw.line(screen, c.BLACK, (self.x, self.y + self.size),
                         (self.x + self.size, self.y + self.size))  # bottom


class Maze:
    def __init__(self, cols, rows):
        self.maze = [[Cell(i * c.SIZE, j * c.SIZE, False) for j in range(rows)] for i in range(cols)]

    def generate_maze(self):
        x = random.randint(0, c.COLS)
        y = random.randint(0, c.ROWS)
        self.gen_maze_helper(x, y)
        """
        lets use recursion!
        choose random cell
        go in a random direction 
        do this until there is no direction that hasn't been visited
        by default this will climb back up the class stack until we are back at the starting cell!
        """

    def gen_maze_helper(self, x, y):

        if x + 1 > c.COLS or y + 1 > c.ROWS or x < 0 or y < 0 or self.maze[x][y].visited:
            return False
        else:
            self.maze[x][y].visited = True
            self.draw_maze(c.SCREEN, c.COLS, c.ROWS, False)
            pygame.display.flip()

            direction = [
                self.gen_maze_helper(x + 1, y),
                self.gen_maze_helper(x - 1, y),
                self.gen_maze_helper(x, y + 1),
                self.gen_maze_helper(x, y - 1)
            ]
            opt = random.choice(direction)

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
