import ReadObj
ReadObj.GetAllInfo()
from random import *

assen_omgedraaid = True
factor = 100

random_colors = False
colors_txt = True
colors_mtl = False
def assenstelsel_wijzigen(input):
    """
    Autocad assen omzetten naar openGL assen
    """

    for vlak in input:
        for point in vlak:
            x0 = point[0]
            y0 = point[1]
            z0 = point[2]
            point[0] = y0
            point[1] = z0
            point[2] = -x0
    return input

def get_random_colors(n):
    """
    returns n tuples in a tuple, each tuple containing 3 values in range [0-1)
    """
    colors = ()
    for i in range(len(input_list)):
        colors += ((random(), random(), random()),)
        # colors += ((0.7,0.56,0.56),)
    return colors

input_list = ReadObj.GetAllFaces()
if assen_omgedraaid:
    input_list = assenstelsel_wijzigen(input_list)

if random_colors:
    colors = get_random_colors(len(input_list))
elif colors_txt:
    color_file = open("colors.txt","r")
    colors = []
    for line in color_file:
        R, G, B = line.split()
        colors.append([factor*float(R),factor*float(G),factor*float(B)])
elif colors_mtl:
    absorb = ReadObj.GetAbsorb()
    colors = []
    for surface_color in absorb:
        absorb_R = surface_color[0]
        absorb_G = surface_color[1]
        absorb_B = surface_color[2]
        # print("absorb:",(absorb_x,absorb_y,absorb_z))
        RGB = [1-absorb_R,1-absorb_G,1-absorb_B]
        colors.append(RGB)

