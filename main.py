import sys
import pygame
import maze as m
from maze_controls import Button
from wrapper import Wrapper
import constants as c
from sys import exit


def main():
    pygame.init()
    sys.setrecursionlimit(20000)
    pygame.display.set_caption("Maze Generator")

    maze = m.Maze()
    gen_button = Button(480, 600, 200, 50)
    maze_gen_box = Button(260, 300, 40, 40)
    backtrack_box = Button(260, 350, 40, 40)
    size_slider = Button(360, 540, 440, 40)
    stage = 1
    coordinates_clicked = []
    generated = is_delay = False
    highlight_backtracking = watch_generation = watch_path = True

    while True:
        Wrapper.SCREEN.fill(c.WHITE)
        maze.draw_maze()

        if not generated:
            gen_button.draw()
            backtrack_box.draw()
            maze_gen_box.draw()
            # size_slider.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # replace with is_pressed function
                if maze_gen_box.rect.collidepoint(pygame.mouse.get_pos()) and stage == 1:
                    watch_generation = not watch_generation

                # replace with is_pressed function
                if backtrack_box.rect.collidepoint(pygame.mouse.get_pos()) and stage == 1:
                    highlight_backtracking = not highlight_backtracking

                # replace with is_pressed function
                if gen_button.rect.collidepoint(pygame.mouse.get_pos()) and stage == 1:
                    maze.generate_maze(watch_generation)
                    maze.solve_maze(0, 0, Wrapper.COLS - 1, Wrapper.ROWS - 1, highlight_backtracking)
                    stage = 2
                    generated = True
                elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
                    maze.reset_maze()
                    x, y = (pos // Wrapper.SIZE for pos in pygame.mouse.get_pos())
                    # pos is a tuple(x,y), pos is divided and floored
                    maze.maze[x][y].color = c.LIGHT_RED
                    coordinates_clicked.append((x, y))
                    if len(coordinates_clicked) == 2:
                        maze.solve_maze(*coordinates_clicked[0], *coordinates_clicked[1])
                        coordinates_clicked.clear()
        pygame.display.update()


if __name__ == "__main__":
    main()

# basically call this same point and pass in where the user clicks, should probably
# pass in the end point as well as the start since that will now be a variable
# the way to find an x,y coord is: how many times can the size "fit" into that location
# ie size = 25, location = 55.6, x = 2
# UI Ideas:
# Generate button
# Size slider : 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 200 400
# Generation option?
# Checkbox to watch maze generation and maze solving algorithm
# Checkbox to highlight dead-end encounters

