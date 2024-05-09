import os

import pygame
from sys import exit
import maze as m

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Screen size is resizeable so it fits on any display
pygame.display.set_caption("Maze Generator")  # Naming the window to fit my game
clock = pygame.time.Clock()  # A clock to keep an eye on framerate
cell = m.Cell(50, 50, 50)

while True:

    screen.fill((255, 255, 255))
    cell.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)  # the framerate ceiling is 60fps
