import random
import math
from scipy.spatial import Delaunay
from Classes import Vector, Polygon
import matplotlib.pyplot as plt
import numpy as np

PLOT2D = False
### Important constants
MIN_EDGE_STEP = 0.5             # step on the edges to take, can be smaller

IN_FACE_DENSITY = 1000          # Random: number of random points

IN_FACE_STEP = MIN_EDGE_STEP    # Rasterization: step to take in x and y

MAX_AREA = 1                    # Recursive: max area after meshing

IN_FACE_NUM_RADII = 10          # Central: number of different radii to take
IN_FACE_NUM_CIRCLE_POINTS = 10  # Central: number of points per radius
IN_FACE_RANDOM_EXTRAS = 100     # Central: number of extra random points to place
MIN_RADIUS = 0.1                # Central: minimum radius to start from

def SetConstants(max_area=MAX_AREA, min_edge_step=MIN_EDGE_STEP,
                 in_face_step=IN_FACE_STEP,in_face_density=IN_FACE_DENSITY, plot=False):
    global MAX_AREA, MIN_EDGE_STEP, IN_FACE_STEP, IN_FACE_DENSITY, PLOT2D
    MAX_AREA = max_area
    MIN_EDGE_STEP = min_edge_step
    IN_FACE_STEP = in_face_step
    IN_FACE_DENSITY = in_face_density
    PLOT2D = plot
    return

def is_equal_point(p1, p2):
    E = 0.0001
    if (abs(p1[0] - p2[0]) < E) and (abs(p1[1] - p2[1]) < E):
        return True
    else:
        return False

def DivideEdge(face, min_edge_step):
    vertices = face.points # Convert Polygon to point list
    points_on_edge = list()

    for i in range(len(vertices)):
        current = vertices[i]
        next = vertices[(i+1) % len(vertices)]

        v_to_next = Vector(next[0] - current[0], next[1] - current[1])
        factor = math.ceil(v_to_next.length / min_edge_step)
        v_step = Vector(v_to_next.X / factor, v_to_next.Y / factor)

        new_point = list(current)
        while not (is_equal_point(new_point, next)):
            new_point[0] = round(new_point[0] + v_step.X, 7)
            new_point[1] = round(new_point[1] + v_step.Y, 7)

            points_on_edge.append(list(new_point))

    return points_on_edge

def AddPointsInFaceRandom(face, edge_points, density):
    for i in range(density):
        point = [random.uniform(face.minX, face.maxX), random.uniform(face.minY, face.maxY)]
        if (face.Contains(point)):
            edge_points.append(point)
        else:
            i -= 1
    return

def AddPointsInFaceRaster(face, edge_points, step):
    # in omhullende rechthoek punten zetten en dan enkelbijhouden welke in de Polygon liggen
    # of met in uniforme cirkel
    # of in circel werken met ofwel concentratie in het centrum of aan de randen

    # To be sure
    step = abs(step)

    point = [face.minX, face.minY]

    while (point[1] <= face.maxY):
        point[0] = round(point[0] + step, 7)

        # If X goes beyond outer rectangle, move one line up
        if (point[0] > face.maxX):
            point[1] = round(point[1] + step, 7)
            point[0] = face.minX

        if (face.Contains(point)):
            edge_points.append(list(point))
    return

def AddPointsInFaceCentral(face, edge_points, centres, num_radii, num_points_in_circle, num_random_extras):
    """
        Centra should be defined as [(x,y), inverse]
    """
    dist = lambda p1, p2 : math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    # Using chebychev points create central densities or edge densities
    for centre in centres:
        max_radius = max(map(lambda p : dist(p, centre[0]),\
            [(face.minX,face.minY), (face.minX,face.maxY), (face.maxX,face.minY), (face.maxX,face.maxY)]))
        # Add centre point
        if (face.Contains(centre[0])):
            edge_points.append(centre[0])

        # Add circles around centre
        for i in range(num_radii):
            cheby_point = math.cos(math.pi*(i+1)/(2*num_radii))
            if (centre[1] == False): # central density
                cheby_point = 1 - cheby_point
            radius = cheby_point * max_radius

            if (radius < MIN_RADIUS):
                continue

            for i in range(num_points_in_circle):
                h = 2 * math.pi * i / num_points_in_circle
                new_point = [centre[0][0] + radius * math.cos(h),centre[0][1] + radius * math.sin(h)]
                if (face.Contains(new_point)):
                    edge_points.append(new_point)
    AddPointsInFaceRandom(face, edge_points, num_random_extras)
    return

def CreateTriangulation(all_points):
    if not isinstance(all_points, np.ndarray):
        all_points = np.array(all_points)

    triangulation = Delaunay(all_points)

    if (PLOT2D):
        Plot2DTri(all_points, triangulation)

    all_faces = list()
    for i in range(len(triangulation.simplices)):
        all_faces.append(list(map(lambda x : list(all_points[x]), triangulation.simplices[i])))

    return all_faces

def Triangulate(face):
    """
        Returns a list of all triangles that are made
    """

    # Create polygon
    p_face = Polygon(face)

    # Divide the edges
    points = DivideEdge(p_face, MIN_EDGE_STEP)

    # Add points to the center
    AddPointsInFaceRaster(p_face, points, IN_FACE_STEP)

    # Create and return the triangulation
    return CreateTriangulation(points)

## OPTION 2
def DividePolygon(face, n):

    if (n > face.num_points):
        n = face.num_points

    points = face.ToList()

    # Sort connecting lines by lentgh
    length = lambda line: \
        -math.sqrt((points[line[0]][0]-points[line[1]][0])**2+(points[line[0]][1]-points[line[1]][1])**2)
    by_lentgh = sorted([(i, (i + 1) % face.num_points) for i in range(face.num_points)], key=length)

    # Add the centers of connecting lines, starting with the biggest one
    for i in range(n):
        p1 = points[by_lentgh[i][0]]
        p2 = points[by_lentgh[i][1]]
        points.append([(p1[0]+p2[0])/2, (p1[1]+p2[1])/2])

    # Triangulate the points
    tri = Delaunay(np.array(points))

    # Get the seperate faces
    #print(points, tri.simplices)
    return list(map(lambda simplex: [list(points[vertex]) for vertex in simplex], tri.simplices))

def TriangulateRecursive(face, maxArea=None, first=True):

    if (maxArea == None):
        maxArea = MAX_AREA

    if maxArea <= 0.00001:
        raise ValueError("Precision to big")

    if not isinstance(face, Polygon):
        face = Polygon(face)

    face_area = face.Area()
    if (face_area == 0):
        return None
    if (face_area <= maxArea):
        return [face.ToList()]

    new_faces = DividePolygon(face, math.floor(face_area/maxArea))

    result = list()
    for face in new_faces:
        deeper = TriangulateRecursive(face, maxArea, False)
        if (deeper != None):
            result.extend(deeper)

    if (first and PLOT2D):
        Plot2DMesh(result)

    return result

## EXTRA
def Plot2DTri(points, triangulation):
    plt.triplot(points[:,0], points[:,1], triangulation.simplices.copy())
    plt.show()
    return

def Plot2DMesh(faces):
    for face in faces:
        plt.triplot(list(map(lambda v : v[0], face)), list(map(lambda v : v[1], face)), np.array([[0,1,2]]))
    plt.show()