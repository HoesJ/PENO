
epsilon = 0.001

def isBetween(p, line):
    same = True
    i = 0
    while same:
        if line[0][i] == line[1][i]:
            i += 1
        else:
            same = False
    l1 = max(line[0][i], line[1][i])
    l2 = min(line[0][i], line[1][i])
    return (p[i] < l1 and p[i] > l2)

def inSamePlane(a, b, c, i, j):
    coefT = (b[j] - a[j])
    coefN = (b[i] - a[i])
    if coefN == 0:
        if coefT == 0:
            return True
        i, j = j, i
        coef = 0
    else:
        coef = coefT / coefN
    cte = a[j] - coef * a[i]
    return c[j] == coef * c[i] + cte

# Given point and surface are in the same plate.
def isInSurface(p, surface):
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
def is_visible(surfaces, x, y, source=None, target=None):
    for surface in surfaces:
        if surface != source and surface != target:
            x1, y1, z1 = x[0], x[1], x[2]
            x2, y2, z2 = y[0], y[1], y[2]
            u1, v1, w1 = surface[0][0], surface[0][1], surface[0][2]
            u2, v2, w2 = surface[1][0], surface[1][1], surface[1][2]
            u3, v3, w3 = surface[2][0], surface[2][1], surface[2][2]
            n1 = (v2 - v1) * (w3 - w1) - (w2 - w1) * (v3 - v1)
            n2 = (w2 - w1) * (u3 - u1) - (u2 - u1) * (w3 - w1)
            n3 = (u2 - u1) * (v3 - v1) - (v2 - v1) * (u3 - u1)
            dT = (u1 - x1) * n1 + (v1 - y1) * n2 + (w1 - z1) * n3
            dN = (x2 - x1) * n1 + (y2 - y1) * n2 + (z2 - z1) * n3
            if dN != 0 :
                d = dT / dN
                Point = [d * (x2 - x1) + x1, d * (y2 - y1) + y1, d * (z2 - z1) + z1]
                if isBetween(Point, [x, y]) and isInSurface(Point, surface):
                    return 0
            elif dT == 0:
                return 0
    return 1
