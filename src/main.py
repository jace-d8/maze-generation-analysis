import sys
import pygame
from game import Game
from maze import Maze


def main():
    pygame.init()
    sys.setrecursionlimit(99999)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()

