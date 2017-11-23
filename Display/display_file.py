from surfaces_with_colors import *
from draw_function import *
from spectator_class import *
import time
nb_surfaces = len(input_list)

print("aantal_vlakken:",nb_surfaces)

movement_speed = .2

forward_button = 'w'
backward_button = 's'
left_strafe_button = 'a'
right_strafe_button = 'd'
fly_up_button = 'f'
fly_down_button = 'c'
stop_key = 'q'

start_x = 0
start_y = 0
start_z = 0

fps = Spectator()
fps.simple_camera_pose(start_x,start_y,start_z)

while fps.loop():
    draw(input_list,colors,0,nb_surfaces)
    fps.controls_3d(movement_speed,0, forward_button, backward_button, left_strafe_button, right_strafe_button,fly_down_button,fly_up_button)
    if fps.keys[stop_key]: break