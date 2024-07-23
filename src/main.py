import sys
import pygame
from src.game import Game
from src.maze import Maze


# potentially add feature where button auto checks at a certain size
# need x button for analysis screen, need to make sure you can't click thru analysis screen
# need to make sure analysis button can only be pressed once
# shannons entropy as y, cell size as x?
def main():
    pygame.init()
    sys.setrecursionlimit(99999)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()
