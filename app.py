import pygame
from pygame.locals import *
import math

from py3d import *

# Setup pygame
pygame.init()
pygame.font.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Nick\'s 3D Engine')
clock = pygame.time.Clock()

# Begin game loop
running = True
while running:

    # Check for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    pygame.draw.rect(screen, (0, 0, 0), Rect(0, 0, width, height))

    # Create 3d object
    mesh = Mesh(triangles = [

        # South
        Triangle(vectors = [
            Vec3D(0, 0, 0), Vec3D(0, 1, 0), Vec3D(1, 1, 0)
        ]),
        Triangle(vectors = [
            Vec3D(0, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 0, 0)
        ]),

        # East
        Triangle(vectors = [
            Vec3D(1, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 1, 1)
        ]),
        Triangle(vectors = [
            Vec3D(1, 0, 0), Vec3D(1, 1, 1), Vec3D(1, 0, 1)
        ]),

        # North
        Triangle(vectors = [
            Vec3D(1, 0, 1), Vec3D(1, 1, 1), Vec3D(0, 1, 1)
        ]),
        Triangle(vectors = [
            Vec3D(1, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 0, 1)
        ]),

        # West
        Triangle(vectors = [
            Vec3D(0, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 1, 0)
        ]),
        Triangle(vectors = [
            Vec3D(0, 0, 1), Vec3D(0, 1, 0), Vec3D(0, 0, 0)
        ]),

        # Top
        Triangle(vectors = [
            Vec3D(0, 1, 0), Vec3D(0, 1, 1), Vec3D(1, 1, 1)
        ]),
        Triangle(vectors = [
            Vec3D(0, 1, 0), Vec3D(1, 1, 1), Vec3D(1, 1, 0)
        ]),

        # Bottom
        Triangle(vectors = [
            Vec3D(1, 0, 1), Vec3D(0, 0, 1), Vec3D(0, 0, 0)
        ]),
        Triangle(vectors = [
            Vec3D(1, 0, 1), Vec3D(0, 0, 0), Vec3D(1, 0, 0)
        ]),
    ])

    # Projection Matrix
    fNear = 0.1
    fFar = 1000.0
    fFov = 90.0
    fFovRad = 1.0 / math.tan(fFov * 0.5 / 180.0 * math.pi)
    fAspectRatio = float(width) / float(height)

    mat4x4 = Matrix4x4(matrix = [
        [ fAspectRatio * fFovRad, 0.0,     0.0,                              0.0 ],
        [ 0.0,                    fFovRad, 0.0,                              0.0 ],
        [ 0.0,                    0.0,     fFar / (fFar - fNear),            1.0 ],
        [ 0.0,                    0.0,     (-fFar * fNear) / (fFar - fNear), 0.0 ]
    ])

    # Draw triangles 
    for tri in mesh.triangles:
        
        triProjected, triTranslated = Triangle(), tri

        # translate the triangles away from "player head"
        triTranslated.vectors[0].z = tri.vectors[0].z + 3.0
        triTranslated.vectors[1].z = tri.vectors[1].z + 3.0
        triTranslated.vectors[2].z = tri.vectors[2].z + 3.0

        # projection, normalise
        triProjected.vectors[0] = Matrix4x4.MultipleMatrixVector(tri.vectors[0], mat4x4)
        triProjected.vectors[1] = Matrix4x4.MultipleMatrixVector(tri.vectors[1], mat4x4)
        triProjected.vectors[2] = Matrix4x4.MultipleMatrixVector(tri.vectors[2], mat4x4)

        # scale back into width & height
        triProjected.vectors[0].x += 1.0; triProjected.vectors[0].y += 1.0
        triProjected.vectors[1].x += 1.0; triProjected.vectors[1].y += 1.0
        triProjected.vectors[2].x += 1.0; triProjected.vectors[2].y += 1.0

        triProjected.vectors[0].x *= 0.5 * float(width); triProjected.vectors[0].y *= 0.5 * float(height); 
        triProjected.vectors[1].x *= 0.5 * float(width); triProjected.vectors[1].y *= 0.5 * float(height); 
        triProjected.vectors[2].x *= 0.5 * float(width); triProjected.vectors[2].y *= 0.5 * float(height); 


        pygame.draw.polygon(screen, (255,255,255), [
            ( triProjected.vectors[0].x, triProjected.vectors[0].y ),
            ( triProjected.vectors[1].x, triProjected.vectors[1].y ),
            ( triProjected.vectors[2].x, triProjected.vectors[2].y )
        ], 2)


    # Update the screen
    pygame.display.update()
    clock.tick(60)