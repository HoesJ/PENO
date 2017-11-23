from OpenGL.GL import *
from OpenGL.GLU import *

def draw(surfaces,colors, start, end):
    glBegin(GL_TRIANGLES)
    # x = 0
    for i in range(start, end):
        surface = surfaces[i]
        for vertex in surface:
            # glColor3fv(colors[x])  # RGB constante van 0 tot 1
            glColor3fv(colors[i])  # RGB constante van 0 tot 1
            glVertex3fv(vertex)
        # x += 1
    glEnd()