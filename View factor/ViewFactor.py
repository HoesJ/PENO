import math
import random
from multiprocessing import current_process

import Visibility
import VectorCalc
import ReadObj_

random.seed()

def surface_polygon(p1, p2, p3, p4=None):
    surface = 0
    if p4 is None:
        directions = VectorCalc.directions(p1, p2, p3)
        cos_angle = VectorCalc.cos_angle_between(directions[0], directions[1])
        sin_angle = math.sqrt(1-cos_angle**2)
        distance1 = VectorCalc.distance_between(p1, p3)
        distance2 = VectorCalc.distance_between(p2, p3)
        surface = 0.5 * sin_angle * distance1 * distance2
    else:
        pass  # moesten het vierhoeken zijn
    return surface

def random_point_in_triangle(p1, p2, p3):
    r1 = random.random()
    r2 = random.random()
    point = [0, 0, 0]
    if len(p1) != len(p2) != len(p3) != 3:
        print("invalid input in random_point_in_triangle")

    sqrt_r1 = math.sqrt(r1)
    for i in range(3):
        point[i] = (1 - sqrt_r1) * p1[i] + sqrt_r1 * (1 - r2) * p2[i] + r2 * sqrt_r1 * p3[i] ##################### TESTIT
    return point

def view_factor(surfaces, p1, p2, p3, q1, q2, q3, N):  # FROM P TO Q
    surface_q = surface_polygon(q1, q2, q3)
    integrand = 0
    for i in range(N):
        p = random_point_in_triangle(p1, p2, p3)
        q = random_point_in_triangle(q1, q2, q3)

        if (Visibility.is_visible(surfaces, p, q, [p1, p2, p3], [q1, q2, q3]) == 0):
            continue # Don't calculate the rest

        r = VectorCalc.distance_between(p, q)
        line = VectorCalc.direction_between(p, q)
        normal_p = VectorCalc.normal(p1, p2, p3)
        normal_q = VectorCalc.normal(q1, q2, q3)
        cos_angle_p = VectorCalc.cos_angle_between(line, normal_p)
        cos_angle_q = VectorCalc.cos_angle_between(line, normal_q)

        integrand += abs(cos_angle_p * cos_angle_q / (math.pow(r,2) * math.pi))
    return (integrand * surface_q) / N

def run_everything_from_P_to_Q(index_polygon_Q, sequence, N):  # FROM P TO Q
    """Returns a list with on each index P the viewfactor from polygon P to Q.
    The index P has the same index as polygon P has in the input sequence."""
    from_P_to_Q = []
    q1, q2, q3 = sequence[index_polygon_Q]
    for index_polygon_P in range(len(sequence)):
        p1, p2, p3 = sequence[index_polygon_P]
        #q1, q2, q3 = sequence[index_polygon_Q] -----> Moet niet elke loop gebeuren dus heb ik verplaatst naar voor de loop
        from_P_to_Q.append(view_factor(sequence, p1, p2, p3, q1, q2, q3, N))
    return from_P_to_Q

def run_everything(all_faces, start, end, N, sender=None):
    """
    Returns a list with on each index a list of the viewfactor of every polygon
    to the polygon at the same index in the input sequence
    """
    if (start < 0):
        raise ValueError("Uncorrect start value")

    if (end > len(all_faces)):
        raise ValueError("Uncorrect end value")

    everything = []
    for index_list_for_Q in range(start, end):
        print("{0}: {1}% --- from {2} -> {3}".format(current_process().name, round((index_list_for_Q-start)/(end-start)*100,1), start, end))
        everything.append(run_everything_from_P_to_Q(index_list_for_Q, all_faces, N))

    if (sender == None):
        return everything
    else:
        sender.send(everything)

def Export(result, time=None):
    file = open("viewmatrixMulti.txt", "w+")

    if (time != None):
        file.write("# Processing time: {0}\n".format(time))
    
    for row in range(len(result)):
        for col in range(len(result[0])):
            line = "{0} {1} {2}".format(row, col, result[row][col])
            file.write(line + "\n")
