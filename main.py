# First GitHub Commit!
import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

# idea
"""
The Maze -
The maze will be a 100 x 100 "grid"(MST?) of set vertices, the walls will be the 
edges connecting the vertices, the randomization of edges will be done via Kruskals
Algorithm(kosarju's algor and prims are also candidates but i forgot how they work)
Solving -
Should be the easier part of the program; will use recursion or a stack and store each path taken
in an array to display later
Graphics - 
The hard part
"""
