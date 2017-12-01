import Visibility

def GetLightDirections(all_surfaces, lights):

    normals1 = dict()
    normals2 = dict()
    normals3 = dict()
    done = GetLightDirectionsOnce(all_surfaces, lights, normals1)
    done = GetLightDirectionsOnce(all_surfaces, done, normals2)
    GetLightDirectionsOnce(all_surfaces, done, normals3)
    return normals1, normals2, normals3

def GetLightDirectionsOnce(all_surfaces, lights, normals=dict()):
    # k = tuple(map(lambda point : tuple(point), lights[0]))
    # normals[k] = [-1,0,0]
    surfaces_done = list(lights)

    for light in lights:
        for target in all_surfaces:
            target_key = tuple(map(lambda point : tuple(point), target))
            if (target_key in normals):
                continue

            direction = SearchSense(all_surfaces, normals, light, target)
            if (direction != None):
                normals[target_key] = direction
                surfaces_done.append(target)

    return surfaces_done


def SearchSense(all_surfaces, normals, source, target):
    source_center = [(source[0][0] + source[1][0] + source[2][0])/3,
                     (source[0][1] + source[1][1] + source[2][1])/3,
                     (source[0][2] + source[1][2] + source[2][2])/3]
    target_center = [(target[0][0] + target[1][0] + target[2][0])/3,
                     (target[0][1] + target[1][1] + target[2][1])/3,
                     (target[0][2] + target[1][2] + target[2][2])/3]

    if (not Visibility.is_visible(all_surfaces, source_center, target_center, source, target, normals)):
        return None

    direction1 = list()
    direction2 = list()
    connection = list()
    for i in range(3):
        direction1.append(target[1][i]-target[0][i])
        direction2.append(target[2][i]-target[0][i])
        connection.append(source_center[i]-target_center[i])

    target_normal = cross_product(direction1, direction2)

    dot = scal_prod(connection, target_normal)
    if (dot == 0):
        print("Loodrechte vlakken ???")
        return None
    else:
        sign = dot/abs(dot)
        return list(map(lambda x : sign*x, target_normal))

####################################### HELPERS
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