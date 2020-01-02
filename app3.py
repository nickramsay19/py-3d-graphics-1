import pygame
from pygame.locals import *
import math

from py3de import *

# Setup pygame
pygame.init()
pygame.font.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Nick\'s 3D Engine')

engine = Engine3D(width, height)
cube = Cube(engine, 0, 0, 2, 0, 0, 1)

# Begin game loop
running = True
while running:

    cube.xr += 0.1

    # Check for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    pygame.draw.rect(screen, (0, 0, 0), Rect(0, 0, width, height))

    # Draw triangles 
    for triangle in cube.ToTriangleList():
        pygame.draw.polygon(screen, (255,255,255), [
            (triangle.vectors[0].x, triangle.vectors[0].y),
            (triangle.vectors[1].x, triangle.vectors[1].y),
            (triangle.vectors[2].x, triangle.vectors[2].y)
        ], 2)


    # Update the screen
    pygame.display.update()