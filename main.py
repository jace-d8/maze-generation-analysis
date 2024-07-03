import sys
import pygame
from game import Game
from maze import Maze


def main():
    pygame.init()
    sys.setrecursionlimit(20000)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()

# UI Ideas:
# Size slider : 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 200 400
# Generation option?
# Checkbox to watch maze generation and maze solving algorithm
# Checkbox to highlight dead-end encounters
