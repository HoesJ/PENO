import numpy as np
from scipy.linalg import lu_factor, lu_solve
import ReadObj
from random import randint

light_source_intensity = [0.9,0.9,0.9]
random_colors = True

def random_absorb(RGB_start, RGB_end, RGB_val,length):
    R_start =RGB_start[0]
    G_start =RGB_start[1]
    B_start =RGB_start[2]

    R_end =RGB_end[0]
    G_end =RGB_end[1]
    B_end =RGB_end[2]

    R_val = 1-RGB_val[0]
    G_val = 1-RGB_val[1]
    B_val = 1-RGB_val[2]

    R = [None for i in range(length)]
    G = [None for i in range(length)]
    B = [None for i in range(length)]

    for i in range(length):
        if i >= R_start and i < R_end:
            R[i] = R_val
        else:
            R[i] = 1
        if i >= G_start and i < G_end:
            G[i] = G_val
        else:
            G[i] = 1
        if i >= B_start and i < B_end:
            B[i] = B_val
        else:
            B[i] = 1

    # R[R_start:R_end] = (R_end - R_start)*[R_val]
    # G[G_start:G_end] = (G_end - G_start)*[G_val]
    # B[B_start:B_end] = (B_end - B_start)*[B_val]

    return [R,G,B]

def solve_intensity_matrix(light_source_intensity,random_colors):
    # ReadObj.SetFile(name='mesh_MainProcess.obj', colors='mesh_MainProcess.mtl')
    surfaces = []
    A_rho_RGB = ReadObj.GetAbsorb()
    A_rho_R, A_rho_G, A_rho_B = [R  for (R, G, B) in A_rho_RGB], \
                                [G  for (R, G, B) in A_rho_RGB], \
                                [B  for (R, G, B) in A_rho_RGB]
    N = len(A_rho_R)
    for i in range(N):
        if A_rho_R[i] == 0 and A_rho_G[i] == 0 and A_rho_B[i] == 0:
            surfaces.append(i)
    print("lichtbronnen:",surfaces)

    if random_colors is True:
        RGB_start = [0,0,0]
        RGB_end = [N,N,N]
        RGB_val = [0.3,0.3,0.3]
        length = N
        rhos = random_absorb(RGB_start, RGB_end, RGB_val,length)
        A_rho_R = rhos[0]
        A_rho_G = rhos[1]
        A_rho_B = rhos[2]

    print('A_rho_R : ', A_rho_R)
    print('A_rho_G : ', A_rho_G)
    print('A_rho_B : ', A_rho_B)

    A_F = [[0 for i in range(N)] for j in range(N)]

    file = open('viewmatrix.txt', 'r')
    for line in file:
        if (line[0] == "#"):
            continue
        i, j, F_i_j = line.strip().split(' ')
        i, j, F_i_j = int(i), int(j), float(F_i_j)
        A_F[i][j] = F_i_j

    A_R, A_G, A_B = [[None for i in range(N)] for j in range(N)], \
                    [[None for i in range(N)] for j in range(N)], \
                    [[None for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j:
                A_R[i][j], A_G[i][j], A_B[i][j] = - A_F[i][j] * A_rho_R[i], \
                                                  - A_F[i][j] * A_rho_G[i], \
                                                  - A_F[i][j] * A_rho_B[i]
            else:
                A_R[i][j], A_G[i][j], A_B[i][j] = 1 - A_F[i][j] * A_rho_R[i], \
                                                  1 - A_F[i][j] * A_rho_G[i], \
                                                  1 - A_F[i][j] * A_rho_B[i]


    bR = [0 for i in range(N)]
    for elem in surfaces:
        bR[elem] = light_source_intensity[0]
    bG = [0 for i in range(N)]
    for elem in surfaces:
        bG[elem] = light_source_intensity[1]
    bB = [0 for i in range(N)]
    for elem in surfaces:
        bB[elem] = light_source_intensity[2]

    LU_R, piv_R = lu_factor(A_R)
    LU_G, piv_G = lu_factor(A_G)
    LU_B, piv_B = lu_factor(A_B)


    solution_R, solution_G, solution_B = lu_solve((LU_R, piv_R), bR), \
                                         lu_solve((LU_G, piv_G), bG), \
                                         lu_solve((LU_B, piv_B), bB)
    file = open('colors.txt', 'w+')
    for i in range(len(solution_R)):
        string = "{0} {1} {2}".format(solution_R[i], solution_G[i], solution_B[i])
        file.write(string + "\n")

ReadObj.GetAllInfo()
solve_intensity_matrix(light_source_intensity,random_colors)