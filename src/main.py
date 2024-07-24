import sys  
import pygame
from src.game import Game
from src.maze import Maze


# GRAPH IDEA: entropy over time
# tmr: do some more analysis GUI but other than that I'm fresh out of ideas
def main():
    pygame.init()
    sys.setrecursionlimit(99999)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()
