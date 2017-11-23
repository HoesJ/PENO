import math

def direction_between(p1, p2):
    """richting van p2 naar p1"""
    direction = []
    if len(p2) != len(p1):
        print("invalid input in direction_between")
    for i in range(len(p1)):
        direction.append(p2[i] - p1[i])
    return direction

def distance_between(point1, point2=[0, 0, 0]):
    distance_squared = 0
    if range(len(point1)) != range(len(point2)):
        print("invalid input in distance_between")
    for i in range(len(point1)):
        distance_squared += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance_squared)

def scal_prod(v1, v2):
    scal = 0
    if len(v1) != len(v2):
        print("invalid input in scal_prod")
    for i in range(len(v1)):
        scal += v1[i] * v2[i]
    return scal

def cross_product(v1, v2):
    cross = [0, 0, 0]
    if len(v1) != len(v2) != 3:
        print("invalid input in cross_prod")
    cross[0] = v1[1] * v2[2] - v1[2] * v2[1]
    cross[1] = v1[2] * v2[0] - v1[0] * v2[2]
    cross[2] = v1[0] * v2[1] - v1[1] * v2[0]
    return cross

def cos_angle_between(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print("invalid input in angle_between")
    cos_theta = scal_prod(v1, v2) / (distance_between(v1) * distance_between(v2))
    if cos_theta > 1 or cos_theta < 1:
        cos_theta = round(cos_theta, 5)
    return cos_theta

def directions(v1, v2, v3, v4=None):
    """berekent de 2 richtingsvectoren tussen 3 punten"""

    direction_vectors = [[], []]
    if len(v1) != len(v2) != len(v3):
        print("invalid input in directions")
    for i in range(len(v1)):
        direction_vectors[0].append(v1[i] - v3[i])
        direction_vectors[1].append(v2[i] - v3[i])
    return direction_vectors

def normal(p1, p2, p3, p4=None):
    dir = directions(p1, p2, p3, p4)
    return cross_product(dir[0], dir[1])

#def normalise_vector(v1):
#    normalised = []
#    for i in range(len(v1)):
#        normalised.append(v1[i] / distance_between(v1))
#    return normalised