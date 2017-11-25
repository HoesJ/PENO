import math, sys
import numpy as np
from ReadObj import WriteProgress
from multiprocessing import current_process

def RotationToXZ(face):
    # Calculate the normal vector
    v1 = [face[1][0] - face[0][0], face[1][1] - face[0][1], face[1][2] - face[0][2]]
    v2 = [face[-1][0] - face[0][0], face[-1][1] - face[0][1], face[-1][2] - face[0][2]]
    normal = np.cross(v1, v2)

    if (normal[1] == 0):
        return np.array([[1,0,0],[0,1,0],[0,0,1]])

    # Make sure that the normal vector is aimed upwards
    if (normal[2] < 0):
        normal = -normal

    # Calculate the angle to rotate
    normalXY = normal[:2]
    cos_angle = np.dot(normalXY, np.array([1,0])) / np.linalg.norm(normalXY)
    sin_angle = math.sqrt(1-cos_angle**2)

    # Create rotation matrix around z-axis, counterclockwise
    rotation_matrix_to_x_axis = np.array([[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]])
    # Determine rotation direction
    if (normal[1] > 0):
        rotation_matrix_to_x_axis = np.transpose(rotation_matrix_to_x_axis)

    return rotation_matrix_to_x_axis

def RotationToXY(face):
    # Calculate the normal vector
    v1 = [face[1][0] - face[0][0], face[1][1] - face[0][1], face[1][2] - face[0][2]]
    v2 = [face[-1][0] - face[0][0], face[-1][1] - face[0][1], face[-1][2] - face[0][2]]
    normal = np.cross(v1, v2)

    # Catch special cases
    if (abs(normal[1]) > 0.00000001):
        print("Error, wrong face")
        return None
    if (normal[0] == 0):
        return np.array([[1,0,0],[0,1,0],[0,0,1]])

    # Make sure the normal vector points upwards
    if (normal[2] < 0):
        normal = -normal

    # Calculate the angle of rotation
    normalXZ = np.array([normal[0], normal[2]])
    cos_angle = np.dot(normalXZ, np.array([0,1])) / np.linalg.norm(normalXZ)
    sin_angle = math.sqrt(1-cos_angle**2)

    # Create rotation matrix around y-axis
    rotation_matrix_to_z_axis = np.array([[cos_angle, 0, sin_angle], [0,1,0], [-sin_angle, 0, cos_angle]])
    # Determine the rotation direction
    if (normal[0] > 0):
        rotation_matrix_to_z_axis = np.transpose(rotation_matrix_to_z_axis)

    return rotation_matrix_to_z_axis

def TransformTo2D(face):
    # Get first rotation
    rot1 = RotationToXZ(face)
    # Rotate vertices
    for i in range(len(face)):
        face[i] = list(rot1.dot(face[i]))

    # Get second rotation
    rot2 = RotationToXY(face)
    # Rotate vertices
    for i in range(len(face)):
        face[i] = rot2.dot(face[i])

    # Only keep x,y coordinates
    z_value = face[0][2]
    for i in range(len(face)):
        face[i] = list(face[i][:2])

    return (rot1, rot2, z_value)

def TransformTo3D(face, old_rot1, old_rot2, z_value):
    # Create new rotations
    rot1 = old_rot1.transpose()
    rot2 = old_rot2.transpose()

    # face is a collection of 2D triangles that need to be rotated separately
    for i in range(len(face)):
        for j in range(len(face[i])):
            # First add the z_value to the point
            face[i][j].append(z_value)
            # Then rotate
            face[i][j] = list(rot1.dot(rot2.dot(face[i][j])))
    return

def MeshAll(faces, absorptions, triangulation_function):
    """
        Function returns all the seperate triangles from the created mesh
    """

    print("\n\nmeshing...")

    tri_faces = list()
    tri_absorptions = list()
    tot = len(faces)

    for i in range(len(faces)):
        progress = i / tot
        WriteProgress(progress)

        # Transform the face to 2D and store the used variables
        rot1, rot2, z_value = TransformTo2D(faces[i])

        # Create a triangulation in 2D
        tri = triangulation_function(faces[i])
        if (tri == None):
            continue

        # Retransform the triangulation to 3D
        TransformTo3D(tri, rot1, rot2, z_value)

        # Add the all the triangle to the tri_faces list
        tri_faces.extend(tri)

        # Add the absorptions of the face to a list
        tri_absorptions.extend([absorptions[i] for j in range(len(tri))])

    if (len(tri_faces) != len(tri_absorptions)):
        print("ERROR: tri_faces doesn't match tri_absorptions")
    print("\nOld faces: ", len(faces))
    print("New faces: ", len(tri_faces))
    print("Factor: ", len(tri_faces) / tot)
    return (tri_faces, tri_absorptions)

def ExportMesh(faces, absorptions, triangulation_function, filename="mesh"):
    """
        Exports the created mesh to a file called "mesh.obj"
    """
    tri, absorb = MeshAll(faces, absorptions, triangulation_function)

    name = "{0}.{1}".format(filename, "{0}")

    file = open(name.format("obj"), "w+")
    mtl = open(name.format("mtl"), "w+")

    current_vertex_index = 0
    current_absorb_index = 0
    prev_absorb = None

    for i in range(len(tri)):
        face = tri[i]

        if (prev_absorb == None or prev_absorb != absorb[i]):
            # Write usemtl line
            line = "usemtl " + str(current_absorb_index) + "\n"
            file.write(line)
            line = "newmtl " + str(current_absorb_index) + "\n"
            line += "Kd " + str(round(1-absorb[i][0], 7)) + " " + str(round(1-absorb[i][1], 7)) + " " + str(round(1-absorb[i][2], 7)) + "\n"
            mtl.write(line)
            prev_absorb = absorb[i]
            current_absorb_index += 1

        # Write v line
        for vertex in face:
            line = "v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n"
            file.write(line)
            current_vertex_index += 1

        # Write f line
        num_vertices = len(face)
        line = "f"
        for i in range(num_vertices-1, -1, -1):
            line += " " + str(current_vertex_index-i)
        file.write(line + "\n")

    file.close()
    mtl.close()
