import pygame
import constants as c
import random


class Cell:
    def __init__(self, x, y):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.visited = False
        self.size = c.SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, screen):
        # Draw the cell rectangle
        if not self.visited:
            pygame.draw.rect(screen, c.BLACK, (self.x, self.y, self.size, self.size))
            wall_color = c.WHITE
        else:
            pygame.draw.rect(screen, c.WHITE, (self.x, self.y, self.size, self.size))
            wall_color = c.BLACK
        # Draw the cell borders; if maze path impedes the cell from certain direction, that direction will not be drawn
        if self.walls["top"]:
            pygame.draw.line(screen, wall_color, (self.x, self.y), (self.x + self.size, self.y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, wall_color, (self.x + self.size, self.y), (self.x + self.size, self.y + self.size), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, wall_color, (self.x, self.y + self.size), (self.x + self.size, self.y + self.size), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, wall_color, (self.x, self.y), (self.x, self.y + self.size), 2)


# the problem may be because cells share borders - does that explain why right and down work tho?

class Maze:
    def __init__(self, cols, rows):
        self.maze = [[Cell(i * c.SIZE, j * c.SIZE) for j in range(rows)] for i in range(cols)]

    def generate_maze(self):
        x = random.randint(0, c.COLS - 1)
        y = random.randint(0, c.ROWS - 1)
        self.gen_maze_helper(x, y)

    def gen_maze_helper(self, x, y):

        # check validity of current cell - if invalid return false
        if x + 1 > c.COLS or y + 1 > c.ROWS or x < 0 or y < 0 or self.maze[x][y].visited:
            return False
        else:  # else this cell is valid can be updated to visited
            self.maze[x][y].visited = True

            # draw maze for visuals
            self.draw_maze(c.SCREEN, c.COLS, c.ROWS, False)  # temp
            pygame.display.update()  # temp

        compass = [  # contains direction coords and label
            ((x, y + 1), "down"),
            ((x, y - 1), "up"),
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

            self.gen_maze_helper(newX, newY)  # -- backtrack

    def draw_maze(self, screen, cols, rows, done):
        for i in range(cols):
            for j in range(rows):
                self.maze[i][j].draw(screen)
            if not done:
                pygame.time.delay(25)
                pygame.display.update()

        # this is for the original "animation" - it can be done every cell but gets too slow if there are 100+ cells