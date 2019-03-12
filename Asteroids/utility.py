import math

class Vector2:
    """ Custom 2d vector class """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, r):
        return Vector2(self.x * r, self.y * r)

    def __truediv__(self, r):
        if type(r) == 'int' or type(r) == 'float':
            return Vector2(self.x / r, self.y / r)

    def rotated(self, angle):
        """ Return the rotated vector of a given vector over a given angle (degrees) """
        angle *= math.pi / 180
        return Vector2(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.y * math.cos(angle) - self.x * math.sin(angle)
        )

    def get_perpd(self):
        """ Return the vector perpendicular to the given vector """
        return Vector2(self.y, -self.x)

    def rotate(self, angle, pivot):
        """ Rotate a point over a given angle (radians) around a given pivot point """
        x = self.x - pivot.x
        y = self.y - pivot.y
        cos = math.cos(angle)
        sin = math.sin(angle)
        _x = x * cos + y * sin
        _y = y * cos - x * sin
        self.x = _x + pivot.x
        self.y = _y + pivot.y

    def tupled(self):
        """ Get tupled version of the vector """
        return (int(self.x), int(self.y))

    def normalized(self):
        """ Get the normalized vector """
        length = self.get_length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def get_length(self):
        """ Get the length of the vector """
        return math.sqrt(self.x**2 + self.y**2)

class Algs:
    """ Custom class containing algorithms """
    def __init__(self):
        pass

    @classmethod
    def v2_min(self, V):
        """ Find vector with min length from vector list """
        d = [0, None]
        for i in range(len(V)):
            l = V[i].get_length()
            if d[1] == None or l < d[1]:
                d[1] = l
                d[0] = i

        return V[d[0]]


    @classmethod
    def get_distance_to_segment(self, x, y, x1, y1, x2, y2):
        """ Get the smallest distance from a given point to a given line segment """
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1
        if len_sq != 0: #in case of 0 length line
            param = dot / len_sq

        xx = 0
        yy = 0

        if param < 0:
            xx = x1
            yy = y1
        elif param > 1:
            xx = x2
            yy = y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D

        dx = x - xx
        dy = y - yy

        return math.sqrt(dx * dx + dy * dy)

    @classmethod
    def get_segment_circle_inters(self, p1, p2, o, r):
        """ Find closest intersection point between circle and segment """
        d1 = p2 - p1
        d2 = p1 - o

        a = d1.x**2 + d1.y**2
        b = 2*(d2.x*d1.x + d2.y*d1.y)
        c = (d2.x**2 + d2.y**2) - r**2

        # Calculate discriminant
        disc= b**2-4*a*c

        if disc < 0 or a == 0:
            # No inters
            return None
        else:
            _disc = math.sqrt(disc)

            t1 = (-b - _disc)/(2*a)
            # Only t1 is used here because it is the closest intersection point (because of -disc)
            # Second intersection point can be calculated with t2 = (-b + _disc)/(2*a)

            if t1 >= 0 and t1 <= 1:
                s = p1 + d1 * t1
                return Vector2(int(s.x), int(s.y))
        return None
    
    @classmethod
    def get_distance(self, p1, p2):
        """ Get distance between two points """
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.sqrt(dx*dx + dy*dy)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sum_matrix_float(v, r):
    """ Calculate sum of a matrix and a float """
    a = [None]*len(v)
    for i in range(len(v)):
        a[i] = v[i] + r
    return a

def clamp(min, max, value):
    """ Clamp value between two given values """
    if value < min:
        return min
    elif value > max:
        return max
    return value