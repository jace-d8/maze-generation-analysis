# First GitHub Commit!
import pygame
import maze

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
run = True
node = pygame.Rect(300,250,50,50)


while run:

    pygame.draw.rect(screen, (255, 0, 0), node)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()

# idea
"""
The Maze -
The maze will be a graph of set vertices, the walls will be the 
edges connecting the vertices, the randomization of edges will be done via Kruskals
Algorithm(kosarju's algor and prims are also candidates but i forgot how they work)
Solving -
Should be the easier part of the program; will use recursion or a stack and store each path taken
in an array to display later
Graphics - 
The hard part
"""
