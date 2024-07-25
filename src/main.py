import sys  
import pygame
from src.game import Game
from src.maze import Maze


# GRAPH IDEA: entropy over time
# tmr: today's plans
# make a plotly graph, x cells generated, y being current entropy
# to do so I'm going to have to make a total cells generated count
# I could maybe do a second line of the graph representing perfect entropy which would just be
# log 2 (x) x being the num of valid probabilities in the distribution
def main():
    pygame.init()
    sys.setrecursionlimit(99999)
    pygame.display.set_caption("Maze Generator")
    maze = Maze()
    game = Game()
    game.run(maze)


if __name__ == "__main__":
    main()
