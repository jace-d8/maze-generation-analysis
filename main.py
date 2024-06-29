import sys
import pygame
import maze as m
import constants as c
from sys import exit

"""
Overall great project! I'm impressed with the animation and path finding, good touches!
I also appreciate the comments and the code really wasn't that hard to follow. I do have
a few comments about the structure and some suggestions for best practices.

Comments:
1. Global variables should be avoided and as application size grows the harder it will be to manage
   global variables. An alternative solution would be make an App class for instance and putting all
   the global variables inside there. but for a smaller application the global variables are fine
2. Some of the constants you define are constants. For example the SCREEN constant is actually an 
   object and since that object has methods you are able to change the underlying data, this means
   that SCREEN isn't a constant because the data can be manipulated by method calls
3. This is something small but is a best practice when working with python. You should define a main
   function. See below on how to do this.

other comments about git:
1. you shouldn't commit non essential files. Examples of these are the .idea/, __pycache__, and .DS_Store 
   files/directories. The .idea folder is for editor configuration so it is non essential for a working application.
   The __pycache__ folder is the bytecode of your application and is non essential because the python compiler can 
   recreate the bytecode based on the source code. So you should create a .gitignore file to tell git not to commit these files
2. When developers clone your git repo they expect the main branch to have a working version of the application.
   When working on a new feature create a branch for it and once it is complete you can merge the branch back into main.
   This is just a best practice so that you know you always have a working version of your code
   
I created my own version of this project, if you want to go over my code let me know
check it out at this url: https://github.com/sydney22john/maze_generation
"""

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

def main():
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
         
if __name__ == "__main__":
    main()
