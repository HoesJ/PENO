import sys
import multiprocessing
import numpy

FILEPATH = "None"
MTLPATH = "None"
FILETYPE = "None"
FACTOR = 1

FACES = list()
ABSORB = list()

def SetFile(name, colors="None", factor=FACTOR):
    global FILEPATH, MTLPATH, FACTOR
    FILEPATH = name
    MTLPATH = colors
    FACTOR = factor
    return

def DetermineType():
    global FILETYPE

    file = open(FILEPATH, 'r')
    line = ""
    while (line[0:2] != "f "):
        line = file.readline()

    if (line.find("/") != -1):
        FILETYPE = "SketchUp"
    elif (line.find("//") != -1):
        FILETYPE = "AutoCAD"
    else:
        FILETYPE = "Standard"

    file.close()
    return

def Translate(input, vertices, faces, current_absorption):

    if (input[0:6] == "usemtl"):
        if (MTLPATH == "None"):
            return (0, 0, 0) # No absporbtion = white

        line_to_find = "newmtl" + input[6:]

        mtl = open(MTLPATH, 'r')
        line = mtl.readline()
        while (line != line_to_find):
            line = mtl.readline()

        while (line[0:2] != "Kd"):
            line = mtl.readline()
        mtl.close()
        R,G,B = line[2:].split()
        return (1-float(R), 1-float(G), 1-float(B))

    elif (input[0:2] == "v "):
        x, y, z = str.split(input[2:])
        vertices.append([float(x), float(y), float(z)])

    elif (input[0:2] == "f "):
        points = str.split(input[2:])
        face = list()
        for p in points:
            if (FILETYPE == "SketchUp"):
                face.append(int(p[:p.find("/")]))
            elif (FILETYPE == "AutoCAD"):
                face.append(int(p[:p.find("//")]))
            else:
                face.append(int(p))

        faces.append(face)
        global ABSORB
        ABSORB.append(current_absorption)

    return current_absorption

def CombineFaces(vertices, faces):
    # return list(map(lambda face: list(map(lambda v: vertices[v - 1], face)), faces))
    return list(map(lambda face: list(map(lambda v: list(map(lambda coord: FACTOR*coord, vertices[v - 1])), face)), faces))

def CleanFaces():
    i = 0
    num_checked = 0
    before = len(FACES)
    while i < len(FACES):
        num_checked += 1
        WriteProgress(num_checked/before)

        if (len(FACES[i]) > 3):
            i += 1
            continue
        if (len(FACES[i]) < 3):
            del FACES[i]
            del ABSORB[i]
            continue

        if (FACES[i][0] == FACES[i][1] or FACES[i][1] == FACES[i][2] or FACES[i][2] == FACES[i][0]):
            del FACES[i]
            del ABSORB[i]
            continue

        p1, p2, p3 = FACES[i]
        dir1 = numpy.array([p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]])
        dir2 = numpy.array([p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]])
        if (abs(numpy.cross(dir1, dir2).sum()) < 0.0000001):
            del FACES[i]
            del ABSORB[i]
            continue

        i += 1


    after = len(FACES)

    if (len(ABSORB) != after):
        print("ERROR: ABSORB is incomparable to FACES")

    print("\nBefore: ", before)
    print("After: ", after)
    print("redundancy: ", 1-after/before)

def GetAllInfo():
    global FACES, FACECOLORS

    if not (isinstance(FILEPATH, str)):
        return None

    DetermineType()

    file = open(FILEPATH, 'r')
    print("reading...")
    vertices = []
    faces = []
    cur_abs = (0.0,0.0,0.0)

    for line in file:
        cur_abs = Translate(line, vertices, faces, cur_abs)
    print("combining...")
    FACES = CombineFaces(vertices, faces)
    print("cleaning...")
    CleanFaces()

def GetAllFaces():
    return [[list(point) for point in face] for face in FACES]

def GetAbsorb():
    return list(ABSORB)

def WriteProgress(progress):
    pass

#GetAllInfo()
