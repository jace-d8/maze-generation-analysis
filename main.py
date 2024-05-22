import sys
import pygame
import maze as m
import constants as c
from sys import exit

pygame.init()
sys.setrecursionlimit(8000)
# screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Screen size is resizeable, so it fits on any display
pygame.display.set_caption("Maze Generator")  # Naming the window to fit my game
clock = pygame.time.Clock()  # A clock to keep an eye on framerate
maze = m.Maze()

done = False
while True:

    c.SCREEN.fill(c.WHITE)
    pygame.event.pump()
    maze.draw_maze(c.SCREEN, done)
    done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze.generate_maze()
                maze.solve_maze(0, 0)

    # maze.draw_maze(c.SCREEN, c.COLS, c.ROWS, done)
    clock.tick(60)  # the framerate ceiling is 60fps
    pygame.display.update()
