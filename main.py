import sys
import pygame
import maze as m
import constants as c
from sys import exit

pygame.init()
sys.setrecursionlimit(20000)
# screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Screen size is resizeable, so it fits on any display
pygame.display.set_caption("Maze Generator")  # Naming the window to fit my game
maze = m.Maze()

while True:
    c.SCREEN.fill(c.WHITE)
    maze.draw_maze(c.SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze.generate_maze()
                maze.solve_maze(0, 0)

    pygame.display.update()
