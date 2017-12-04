epsilon = 0.001

def scal_prod(v1, v2):
    scal = 0
    if len(v1) != len(v2):
        print("invalid input in scal_prod")
    for i in range(len(v1)):
        scal += v1[i] * v2[i]
    return scal

def isBetween(p, line):
    same = True
    i = 0
	# if the value of the points on dimesion i are the same, chose the next dimension.
    while same:
        if line[0][i] == line[1][i]:
            i += 1
        else:
            same = False
    l1 = max(line[0][i], line[1][i])
    l2 = min(line[0][i], line[1][i])
    return (p[i] < l1 and p[i] > l2)

# check if the ij projection of the given surface is two dimensional, and not just a line.
def inSamePlane(a, b, c, i, j):
    coefT = (b[j] - a[j])
    coefN = (b[i] - a[i])
    if coefN == 0:
		# if both are 0, the projections of the points a and b on the ij plane are the same.
        if coefT == 0:
            return True
        i, j = j, i
        coef = 0
    else:
        coef = coefT / coefN
    cte = a[j] - coef * a[i]
	# check if the projection of point c is between the projections of a and b
    return c[j] == coef * c[i] + cte

# Check if the given point, which should be on the same plane as the given surface, is inside the borders of the surface using Ray casting algorithm.
def isInSurface(p, surface):
	# Search for the plane where the projection of the surface is not a line.
    if not inSamePlane(surface[0], surface[1], surface[2], 0, 1):
        m, n = 0, 1
    elif not inSamePlane(surface[0], surface[1], surface[2], 0, 2):
        m, n = 0, 2
    else:
        m, n = 1, 2
    throughPoint = False
    s = list(surface)
    s.append(surface[0])
    counter = 0
    y0 = p[n]
    for i in range(len(s) - 1):
        x0 = float("inf")
        x1, x2, y1, y2 = s[i][m], s[i + 1][m], s[i][n], s[i + 1][n]
        if x1 == x2:
            x0 = x1
        elif y1 != y2:
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1
            x0 = (y0 - b) / a
        if x0 < p[m] and isBetween([x0, y0], [[x1, y1], [x2, y2]]):
            counter += 1
        elif (not throughPoint) and (p[m] > x0) and ((x0 == x1 and y0 == y1) or (x0 == x2 and y0 == y2)):
            counter += 1
            throughPoint = True
    if counter % 2 == 0:
        return False
    return True

# Si and Sj: initial surfaces, used to not check visibility on them.
def is_visible(surfaces, source_point, target_point, source=None, target=None, light_directions=None):

    # check visibility
    for surface in surfaces:
        if surface != source and surface != target:
			# xyz coordinates of random points.
            x1, y1, z1 = source_point[0], source_point[1], source_point[2]
            x2, y2, z2 = target_point[0], target_point[1], target_point[2]
			# xyz coordinates of vertex of surface
            u1, v1, w1 = surface[0][0], surface[0][1], surface[0][2]
            u2, v2, w2 = surface[1][0], surface[1][1], surface[1][2]
            u3, v3, w3 = surface[2][0], surface[2][1], surface[2][2]
			# calculate normalvector of surface
            n1 = (v2 - v1) * (w3 - w1) - (w2 - w1) * (v3 - v1)
            n2 = (w2 - w1) * (u3 - u1) - (u2 - u1) * (w3 - w1)
            n3 = (u2 - u1) * (v3 - v1) - (v2 - v1) * (u3 - u1)
			# "Teller" and "Noemer" of variable d, part of the equation of the line between source_point and target_point.
            dT = (u1 - x1) * n1 + (v1 - y1) * n2 + (w1 - z1) * n3
            dN = (x2 - x1) * n1 + (y2 - y1) * n2 + (z2 - z1) * n3
			# If dN == 0: line is parallel to surface. If dT == dN == 0: Line is inside surface.
			# Else: d is real, filling in the equation of the line gives its intersection with the plane of the surface.
            if dN != 0:
                d = dT / dN
                Point = [d * (x2 - x1) + x1, d * (y2 - y1) + y1, d * (z2 - z1) + z1]
				# Surface is between the two points, if the found intersection point is between source_point and target_point, 
				# and is inside of the borders of the surface.
                if isBetween(Point, [source_point, target_point]) and isInSurface(Point, surface):
                    return 0
            elif dT == 0:
                return 0

    #check light direction
    source_key = tuple(map(lambda point: tuple(point), source))
    if (light_directions != None and source_key in light_directions):
        direction = light_directions[source_key]
        connection = list(map(lambda i : target_point[i]-source_point[i], range(3)))
        dot = scal_prod(connection, direction)
        if (dot == 0):
            return 0
        else:
            sign = dot / abs(dot)
            if (sign < 0):
                return 0
    return 1
