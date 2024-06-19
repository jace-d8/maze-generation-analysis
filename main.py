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

clicker_count = 0
# UI Ideas:
# Generate button
# Size slider : 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 200 400
# Checkbox to watch maze generation and maze solving algorithm
# Checkbox to highlight dead-end encounters
# MAYBE try to do the click to cells thing after maze is done solving

while True:
    c.SCREEN.fill(c.WHITE)
    maze.draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze.generate_maze()
                maze.solve_maze(0, 0, c.COLS - 1, c.ROWS - 1)
        if event.type == pygame.MOUSEBUTTONDOWN:  # and count less than 2 (after func runs reset count)
            x, y = (pos // c.SIZE for pos in pygame.mouse.get_pos())  # pos is a tuple(x,y), pos is divided and floored
            # clicker_count += 1
            # if clicker_count == 2:
            #     maze.solve_maze(x, y)
            # reset maze function
            # basically call this same point and pass in where the user clicks, should probably
            # pass in the end point as well as the start since that will now be a variable
            # the way to find an x,y coord is: how many times can the size "fit" into that location
            # ie size = 25, location = 55.6, x = 2

    pygame.display.update()
