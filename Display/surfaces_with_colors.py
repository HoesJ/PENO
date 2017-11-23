import ReadObj
ReadObj.GetAllInfo()
from random import *

assen_omgedraaid = True
factor = 100

random_colors = False
colors_txt = False
colors_mtl = False
test_colors = True
test_color = 500


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
N = len(input_list)

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
        absorb_R = 1-surface_color[0]
        absorb_G = 1-surface_color[1]
        absorb_B = 1-surface_color[2]
        # print("absorb:",(absorb_x,absorb_y,absorb_z))
        RGB = [1-absorb_R,1-absorb_G,1-absorb_B]
        colors.append(RGB)
elif test_colors:
    A_F = [[0 for i in range(N)] for j in range(N)]
    file = open('viewmatrixMulti_15.txt', 'r')
    for line in file:
        if (line[0] == "#"):
            continue
        i, j, F_i_j = line.strip().split(' ')
        i, j, F_i_j = int(i), int(j), float(F_i_j)
        A_F[i][j] = F_i_j

    colors = [[0.5,0,0] for i in range(N)]
    colors[test_color] = [1,1,1]

    for i in range(N):
        if (i != test_color and A_F[test_color][i] != 0):
            colors[i] = (0,0.5,0)

    print(colors[test_color])




