import data as d
from utility import Vector2, Algs
import pygame as pg
import math
import numpy as np

class Spaceship:
    def __init__(self):
        self.pos = Vector2(d.SCREEN_SIZE/2, d.SCREEN_SIZE/2)
        self.points = [Vector2()] * 3
        self.velocity = Vector2()
        self.angular_vel = 0
        self.rotation = 0
        self.dead = False
        self.ast_idx = [1] * len(d.asteroids)

    def draw(self):
        tupled_points = []
        for point in self.points:
            tupled_points.append(point.tupled())

        pg.draw.lines(d.SURFACE, d.NEON_BLUE, True, tupled_points, 2)

    def update(self):
        self.pos += self.velocity * d.SPEED
        self.rotation += self.angular_vel
        self.angular_vel *= d.ANG_DRAG

        self.velocity *= d.DRAG

        self.velocity.x -= math.sin(self.rotation) * d.POWER
        self.velocity.y -= math.cos(self.rotation) * d.POWER

        self.check_boundaries()
        self.check_collision()
        self.update_points_pos()
        self.update_points_rot()
        self.get_closest_ast()

    def update_points_pos(self):
        half_h = d.PLAYER_H / 2
        half_w = d.PLAYER_W / 2
        self.points[0] = self.pos + Vector2(-half_w, half_h)
        self.points[1] = self.pos + Vector2(half_w, half_h)
        self.points[2] = self.pos + Vector2(0, -half_h)

    def turn(self, angle):
        self.angular_vel -= angle * d.TURN_SPEED * 0.001

    def update_points_rot(self):
        for point in self.points:
            point.rotate(self.rotation, self.pos)

    def check_boundaries(self):
        if self.pos.y > d.SCREEN_SIZE:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = d.SCREEN_SIZE

        if self.pos.x > d.SCREEN_SIZE:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = d.SCREEN_SIZE

    def check_collision(self):
        for a in d.asteroids:
            for i in range(len(self.points)):
                j = i+1
                if(i == len(self.points)-1):
                    j = 0
                x1 = self.points[i].x
                y1 = self.points[i].y
                x2 = self.points[j].x
                y2 = self.points[j].y
                l = Algs.get_distance_to_line(a.pos.x, a.pos.y, x1, y1, x2, y2)
                if l - a.rad <= 0:
                    self.die()
                    a.die()

    def get_closest_ast(self):
        ds = []
        for ast in d.asteroids:
            distance = Algs.get_distance(self.pos, ast.pos) - ast.rad
            ds.append(distance)
        a = np.array(ds)
        
        # Get indices of the closest asteroids
        self.ast_idx = np.argpartition(a, -d.CLOSEST_AST_COUNT)[:d.CLOSEST_AST_COUNT].tolist()

    def die(self):
        self.dead = True

    def reset(self):
        self.dead = False
        self.pos = Vector2(d.SCREEN_SIZE/2, d.SCREEN_SIZE/2)
        self.velocity = Vector2()
        self.angular_vel = 0
        self.rotation = 0