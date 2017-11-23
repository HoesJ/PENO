import numpy as np
from scipy.linalg import lu_factor, lu_solve
import ReadObj
from random import randint

rho_multiplication_factor = 1
nb_light_sources = 30
light_source_intensity = 0.9


def solve_intensity_matrix(rho_multiplication_factor, nb_light_sources, light_source_intensity, surfaces):
    # ReadObj.SetFile(name='mesh_MainProcess.obj', colors='mesh_MainProcess.mtl')
    A_rho_RGB = ReadObj.GetAbsorb()
    A_rho_R, A_rho_G, A_rho_B = [R * rho_multiplication_factor for (R, G, B) in A_rho_RGB], \
                                [G * rho_multiplication_factor for (R, G, B) in A_rho_RGB], \
                                [B * rho_multiplication_factor for (R, G, B) in A_rho_RGB]
    # print('A_rho_R : ', A_rho_R)
    # print('A_rho_G : ', A_rho_G)
    # print('A_rho_B : ', A_rho_B)

    N = len(A_rho_R)

    for i in range(N):
        if A_rho_R[i] == 0 and A_rho_G[i] == 0 and A_rho_B[i] == 0:
            surfaces.append(i)

    # A_rho_R, A_rho_G, A_rho_B = [0.1 for i in range(N)], [0.1 for i in range(N)], [0.1 for i in range(N)]
    # A_rho_R[:150], A_rho_G[150:300], A_rho_B[300:N] = [0.5] * 150, [0.5] * 150, [0.5] * (N-300)

    # print('A_rho_R : ', A_rho_R)
    # print('A_rho_G : ', A_rho_G)
    # print('A_rho_B : ', A_rho_B)

    # print('N : ', N)
    A_F = [[0 for i in range(N)] for j in range(N)]

    file = open('viewmatrix.txt', 'r')
    for line in file:
        i, j, F_i_j = line.strip().split(' ')
        i, j, F_i_j = int(i), int(j), float(F_i_j)
        A_F[i][j] = F_i_j
        # print('i : ', i, 'j : ', j, 'F_i_j : ', F_i_j)

    A_R, A_G, A_B = [[None for i in range(N)] for j in range(N)], \
                    [[None for i in range(N)] for j in range(N)], \
                    [[None for i in range(N)] for j in range(N)]
    # print('A_R :  ', A_R)
    for i in range(N):
        for j in range(N):
            # print(i, j)
            if i != j:
                A_R[i][j], A_G[i][j], A_B[i][j] = - A_F[i][j] * A_rho_R[i], \
                                                  - A_F[i][j] * A_rho_G[i], \
                                                  - A_F[i][j] * A_rho_B[i]
            else:
                A_R[i][j], A_G[i][j], A_B[i][j] = 1 - A_F[i][j] * A_rho_R[i], \
                                                  1 - A_F[i][j] * A_rho_G[i], \
                                                  1 - A_F[i][j] * A_rho_B[i]

    # print('A_R : ', A_R)
    # print('A_G : ', A_G)
    # print('A_B : ', A_B)
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
    # print('LU_R : ', LU_R)
    # print('LU_R : ', LU_R)
    # print('LU_G : ', LU_G)

    solution_R, solution_G, solution_B = lu_solve((LU_R, piv_R), bR), \
                                         lu_solve((LU_G, piv_G), bG), \
                                         lu_solve((LU_B, piv_B), bB)
    # print('solution_R : ', solution_R)
    # print('solution_G : ', solution_G)
    # print('solution_B : ', solution_B)

    file = open('colors.txt', 'w+')
    for i in range(len(solution_R)):
        string = "{0} {1} {2}".format(solution_R[i], solution_G[i], solution_B[i])
        file.write(string + "\n")


solve_intensity_matrix(rho_multiplication_factor=1,
                       nb_light_sources=3,
                       light_source_intensity=[0.5,0.5,0.5],
                       surfaces=[1,2,3,4,5,6,7,8,9])