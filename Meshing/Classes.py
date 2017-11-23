import math
import numpy as np

class Vector:

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.length = self.Length()

    def Length(self):
        return math.sqrt(self.X * self.X + self.Y * self.Y)

    def Copy(self):
        return Vector(self.x, self.y)


class Polygon:

    def __init__(self, points):
        self.points = points
        self.num_points = len(points)

        self.minX = min(points)[0]
        self.maxX = max(points)[0]
        self.minY = min(points, key=lambda x : x[1])[1]
        self.maxY = max(points, key=lambda x : x[1])[1]

    def ToList(self):
        return [list(v) for v in self.points]

    def Center(self):
        x = sum(map(lambda x : x[0], self.points)) / self.num_points
        y = sum(map(lambda x : x[1], self.points)) / self.num_points
        return [x, y]

    def Area(self):
        area = 0
        for i in range(self.num_points):
            j = (i + 1) % self.num_points
            area += self.points[i][0] * self.points[j][1]
            area -= self.points[i][1] * self.points[j][0]
        area = abs(area) / 2
        return area

    def Contains(self, point):
        # For a triangle use determinant method
        if (self.num_points == 3):

            sign = lambda p1,p2,p3 : (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

            b1 = sign(point, self.points[0], self.points[1]) < 0
            b2 = sign(point, self.points[1], self.points[2]) < 0
            b3 = sign(point, self.points[2], self.points[0]) < 0

            return (b1 == b2 and b2 == b3)

        else:
            crossed_lines = 0

            for i in range(self.num_points):
                current = self.points[i]
                next = self.points[(i+1) % self.num_points]

                # Check if line is in range of crossing
                # We draw a horizontal ray, so only y-values need to be checked
                # Exception: when the y-coordinate is equal to a vertex' y-coordinate, it is counted for both edges
                # To skip this only one comparisson in with the equal sign (< and >=) or (<= and >) not (<= and >=)
                if (min(current[1], next[1]) < point[1]) and (max(current[1], next[1]) >= point[1]):
                    v_to_next = [next[0] - current[0], next[1] - current[1]]
                    v_to_start = [self.minX - 1 - current[0], point[1] - current[1]]
                    v_to_end = [point[0] - current[0], point[1] - current[1]]

                    cross_prod_to_start = np.cross(v_to_next, v_to_start)
                    cross_prod_to_end = np.cross(v_to_next, v_to_end)

                    # Point lies on edge
                    if cross_prod_to_end == 0:
                        return True

                    # Get signs
                    a = cross_prod_to_start / abs(cross_prod_to_start)
                    b = cross_prod_to_end / abs(cross_prod_to_end)

                    if (a != b):
                        crossed_lines += 1

            return not ((crossed_lines % 2) == 0)