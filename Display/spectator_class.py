from __future__ import division
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import math
import time


class Spectator:
    def __init__(self, w=1540, h=800, fov=75):
        pygame.init()
        pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        aspect = w / h
        gluPerspective(fov, aspect, 0.1, 100000.0)
        glMatrixMode(GL_MODELVIEW)


    def simple_camera_pose(self,start_x,start_y,start_z):
        """ Pre-position the camera (optional) """


        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(numpy.array([0.741, -0.365, 0.563, 0, 0, 0.839, 0.544,
                                   0, -0.671, -0.403, 0.622, 0, -start_y, -start_z, start_x, 1]))

    def loop(self):
        pygame.display.flip()
        pygame.event.pump()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.keys = dict((chr(i), int(v)) for i, v in \
                         enumerate(pygame.key.get_pressed()) if i < 256)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        return True

    def controls_3d(self,move_speed = 0.1,mouse_button=0, w_key='w', s_key='s', a_key='a', d_key='d',low_key='c',fly_key='f'):
        """ The actual camera setting cycle """
        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[mouse_button]:
            look_speed = .2
            buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
            c = (-1 * numpy.mat(buffer[:3, :3]) * numpy.mat(buffer[3, :3]).T).reshape(3, 1)
            # c is camera center in absolute coordinates,
            # we need to move it back to (0,0,0)
            # before rotating the camera
            glTranslate(c[0], c[1], c[2])
            m = buffer.flatten()
            glRotate(mouse_dx * look_speed, m[1], m[5], m[9])
            glRotate(mouse_dy * look_speed, m[0], m[4], m[8])

            # compensate roll
            glRotated(-math.atan2(-m[4], m[5]) * \
                      57.295779513082320876798154814105, m[2], m[6], m[10])
            glTranslate(-c[0], -c[1], -c[2])

        # move forward-back or right-left
        # fwd =   .1 if 'w' is pressed;   -0.1 if 's'
        fwd = move_speed * (self.keys[w_key] - self.keys[s_key])
        strafe = move_speed * (self.keys[a_key] - self.keys[d_key])
        fly = move_speed * (self.keys[fly_key] - self.keys[low_key])
        if abs(fwd) or abs(strafe) or abs(fly):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            glTranslate(fwd * m[2], fwd * m[6], fwd * m[10])
            glTranslate(strafe * m[0], strafe * m[4], strafe * m[8])
            glTranslate(0,-fly,0)