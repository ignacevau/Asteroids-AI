import pygame
import math

class Vector2:
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
        return Vector2(self.x / r, self.y / r)

    def get_rotated(self, angle):
        print(angle)
        angle *= math.pi / 180
        return Vector2(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.y * math.cos(angle) - self.x * math.sin(angle)
        )

    def rotate(self, angle, pivot):
        #angle *= math.pi / 180
        x = self.x - pivot.x
        y = self.y - pivot.y
        cos = math.cos(angle)
        sin = math.sin(angle)
        _x = x * cos + y * sin
        _y = y * cos - x * sin
        self.x = _x + pivot.x
        self.y = _y + pivot.y

    def tupled(self):
        return (int(self.x), int(self.y))

class Algs:
    def __init__(self):
        pass

    @classmethod
    def get_distance_to_line(self, x, y, x1, y1, x2, y2):
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
    def get_distance(self, p1, p2):
        dx = p2.x - p1.x
        print(dx)
        dy = p2.y - p1.y
        print(dy)
        return math.sqrt(dx*dx + dy*dy)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sum_matrix_float(v, r):
    a = [None]*len(v)
    for i in range(len(v)):
        a[i] = v[i] + r
    return a

def clamp(min, max, value):
    if value < min:
        return min
    elif value > max:
        return max
    return value