import pygame
import constants as c
import random


class Cell:
    def __init__(self, x, y):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.visited = False
        self.color = c.BLACK
        self.size = c.SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def visit(self):
        self.visited = True
        self.color = c.WHITE

    def mark(self, direction):
        pygame.draw.line(c.SCREEN, c.RED, (self.x, self.y), (self.x + self.size, self.y), 2)

    def draw(self):
        # Draw the cell rectangle
        pygame.draw.rect(c.SCREEN, self.color, (self.x, self.y, self.size, self.size))
        if not self.visited:
            wall_color = c.WHITE
        else:
            wall_color = c.BLACK
        # Draw the cell borders; if maze path impedes the cell from certain direction, that direction will not be drawn
        if self.walls["top"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y), (self.x + self.size, self.y), 2)
        if self.walls["right"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x + self.size, self.y), (self.x + self.size, self.y + self.size),
                             2)
        if self.walls["bottom"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y + self.size), (self.x + self.size, self.y + self.size),
                             2)
        if self.walls["left"]:
            pygame.draw.line(c.SCREEN, wall_color, (self.x, self.y), (self.x, self.y + self.size), 2)


class Maze:
    def __init__(self):
        self.maze = [[Cell(i * c.SIZE, j * c.SIZE) for j in range(c.ROWS)] for i in range(c.COLS)]

    def generate_maze(self):
        x = random.randint(0, c.COLS - 1)
        y = random.randint(0, c.ROWS - 1)
        self.gen_maze_helper(x, y)

    def gen_maze_helper(self, x, y):

        # check validity of current cell - if invalid return false
        if x + 1 > c.COLS or y + 1 > c.ROWS or x < 0 or y < 0 or self.maze[x][y].visited:
            return
        else:  # else this cell is valid can be updated to visited
            self.maze[x][y].visit()

            # draw maze for visuals
            # self.draw_maze(c.SCREEN, False)  # temp
            pygame.display.update()  # temp

        compass = [  # contains direction coords and label
            ((x, y - 1), "up"),
            ((x, y + 1), "down"),
            ((x + 1, y), "right"),
            ((x - 1, y), "left")
        ]
        # choose random direction, if the direction is invalid, remove it and try again
        for (newX, newY), direction in random.sample(compass, len(compass)):
            if 0 <= newX < c.COLS and 0 <= newY < c.ROWS and not self.maze[newX][newY].visited:
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

            self.gen_maze_helper(newX, newY)  # recursive step. If backtracking will occur if-
            # there are more directions available in the loop

    def draw_maze(self, screen, done):
        for i in range(c.COLS):
            for j in range(c.ROWS):
                self.maze[i][j].draw()
            if not done:
                pygame.time.delay(25)
                pygame.display.update()
        # this is for the original "animation" - it can be done every cell but gets too slow if there are 100+ cells

    def solve_maze(self, x, y):
        self.maze[x][y].color = c.RED
        self.draw_maze(c.SCREEN, False)  # temp
        pygame.display.update()  # temp
        compass = [  # the cell walls and the direction needed to move to next cell in said direction
            (self.maze[x][y].walls["top"], (x, y - 1)),
            (self.maze[x][y].walls["bottom"], (x, y + 1)),
            (self.maze[x][y].walls["right"], (x + 1, y)),
            (self.maze[x][y].walls["left"], (x - 1, y))
        ]
        if y == c.ROWS - 1 and x == c.COLS - 1:
            return True # return True if end is reached
        else:
            # choose random direction, if the direction is invalid, remove it and try again
            # backtracking will happen by default if there are more directions available
            for wall, new_direction in random.sample(compass, len(compass)):
                new_x, new_y = new_direction
                if not wall and self.maze[new_x][new_y].color != c.RED:  # if wall is not present go that way
                    if self.solve_maze(*new_direction):  # pass in new direction to function
                        return True  # This will send "True" up the call stack and end the recursion
            self.maze[x][y].color = c.WHITE
            self.draw_maze(c.SCREEN, False)  # temp
            pygame.display.update()  # temp
            return False
        # if we return to start and all surrounding cells have been hit , maze has no exit
