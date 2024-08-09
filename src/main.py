import sys  
import pygame
from src.game import Game
from src.maze import Maze
from tests.test_entropy import run


# GRAPH IDEA: entropy over time
# make a plotly graph, x cells generated, y being current entropy
# to do so I'm going to have to make a total cells generated count
# I could maybe do a second line of the graph representing perfect entropy which would just be
# log 2 (x) x being the num of valid probabilities in the distribution
# could use some graph for direction generation
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
