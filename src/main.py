import sys  
import pygame
from src.game import Game
from src.maze import Maze
from tests.test_entropy import run


def main():
    run()
    pygame.init()
    sys.setrecursionlimit(99999)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()
