import pygame
import maze as m
import constants as c
from sys import exit

pygame.init()

# need to figure out how
# screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Screen size is resizeable so it fits on any display
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Maze Generator")  # Naming the window to fit my game
clock = pygame.time.Clock()  # A clock to keep an eye on framerate
COLS = int(screen.get_width() / c.SIZE)
ROWS = int(screen.get_height() / c.SIZE)
maze = m.Maze(COLS, ROWS)
# Put pygame in constants and declare screen in there because the screen is const
# num of cols = screen.get_width() / size
# num of row = screen.get_height() / size
# screen size will vary so a cast is needed to ensure no floats are created due to the difference

done = False
while True:

    screen.fill(c.WHITE)
    pygame.event.pump()
    maze.draw_maze(screen, COLS, ROWS, done)
    done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(60)  # the framerate ceiling is 60fps
    pygame.display.update()
