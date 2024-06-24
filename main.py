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
coordinates_clicked = []
generated = False
highlight_backtracking = watch_generation = watch_path = True
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
                generated = True

        if event.type == pygame.MOUSEBUTTONDOWN and generated:  # and count less than 2 (after func runs reset count)
            maze.reset_maze()
            x, y = (pos // c.SIZE for pos in pygame.mouse.get_pos())  # pos is a tuple(x,y), pos is divided and floored
            maze.maze[x][y].color = c.LIGHT_RED
            coordinates_clicked.append((x, y))
            if len(coordinates_clicked) == 2:
                maze.solve_maze(*coordinates_clicked[0], *coordinates_clicked[1])
                coordinates_clicked.clear()

        # basically call this same point and pass in where the user clicks, should probably
        # pass in the end point as well as the start since that will now be a variable
        # the way to find an x,y coord is: how many times can the size "fit" into that location
        # ie size = 25, location = 55.6, x = 2

    pygame.display.update()
