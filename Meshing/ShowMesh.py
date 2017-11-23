import pygame
import Meshing, ReadObj
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def dots_to_connect(input_list):
    """
    returns a list of tuples, each tuple contains 2 points to be connected
    """
    vlakken = []

    answer = []

    for vlak in input_list:
        vlakken.append(vlak)

    for vlak in vlakken:
        for i in range(len(vlak)-1):
            answer.append((vlak[i],vlak[i+1]))
        answer.append((vlak[len(vlak)-1],vlak[0]))

    return answer

def Draw(dots):
    glBegin(GL_LINES)

    for pair in dots:
        for dot in pair:
            glVertex3fv(dot)
    glEnd()

def main(dots):
    global pos
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) #notify the display refersh rate and openGL
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0]/display[1]), 0.01, 500.0) #field of view degrees, aspect ratio (width/height), z-near, zz-far ( clipping planes )

    glTranslatef(0.0,0.0,-5) # punt van waar ge kjkt

    glRotatef(0,0,0,0) # rotate code (degrees, x, y ,z)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.2, 0.0, 0.0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.2, 0.0, 0.0)
                if event.key == pygame.K_UP:
                    glTranslatef(0.0, 0.2, 0.0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0.0, -0.2, 0.0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 0.0, 10)
                if event.button == 5:
                    glTranslatef(0.0, 0.0, -10)

        glRotatef(3, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Draw(dots)
        pygame.display.flip()
        pygame.time.wait(10)


def Show(input_list):
    print(input_list)
    dots = dots_to_connect(input_list)
    main(dots)