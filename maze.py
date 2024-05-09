import pygame


class Maze:
    def __init__(self):
        self.maze = {}

    def generate_maze(self, node):
        self.maze[node] = set()

    def draw_maze(self):
        print("todo")


class Cell:
    def __init__(self, x, y, size):  # each cell will need coords to where they are being stored
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        # Draw the cell rectangle
        pygame.draw.rect(screen, (255, 255, 255), (self.x * self.size, self.y * self.size, self.size, self.size))
        # Draw the cell borders
        pygame.draw.line(screen, (0, 0, 0), (self.x * self.size, self.y * self.size),((self.x + 1) * self.size, self.y * self.size))
        pygame.draw.line(screen, (0, 0, 0), ((self.x + 1) * self.size, self.y * self.size), ((self.x + 1) * self.size, (self.y + 1) * self.size))
        pygame.draw.line(screen, (0, 0, 0), ((self.x + 1) * self.size, (self.y + 1) * self.size),  (self.x * self.size, (self.y + 1) * self.size))
        pygame.draw.line(screen, (0, 0, 0), (self.x * self.size, (self.y + 1) * self.size),(self.x * self.size, self.y * self.size))

        # idea
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
