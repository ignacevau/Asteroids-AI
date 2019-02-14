import data as d
from utility import Vector2
import pygame as pg
import random
import math

class Asteroid:
    def __init__(self, spawn_edge):
        # spawn_edge : (1, 2, 3, 4) = (top, right, bottom, left)
        self.dir = Vector2(0, 1)
        self.pos = Vector2()
        self.rad = random.randint(d.AST_MIN_SIZE, d.AST_MAX_SIZE)
        self.speed = random.uniform(d.AST_MIN_SPD, d.AST_MAX_SPD)
        self.dead = False
        self.color = d.WHITE

        self.spawn(spawn_edge)

    def spawn(self, edge):
        s = d.SCREEN_SIZE
        t = random.uniform(0, s)
        if edge == 1:
            self.pos.x = t
            self.pos.y = 0
            self.dir = Vector2(0, 1)
        elif edge == 2:
            self.pos.x = s
            self.pos.y = t
            self.dir = Vector2(-1, 0)
        elif edge == 3:
            self.pos.x = t
            self.pos.y = s
            self.dir = Vector2(0, -1)
        else:
            self.pos.x = 0
            self.pos.y = t
            self.dir = Vector2(1, 0)

        self.dir.rotate(random.uniform(-math.pi/2, math.pi/2), Vector2())        

    def draw(self):
        pg.draw.circle(d.SURFACE, self.color, self.pos.tupled(), self.rad, 1)

    def update(self):
        self.pos += self.dir * self.speed
        self.check_boundaries()

    def check_boundaries(self):
        if self.pos.y > d.SCREEN_SIZE or self.pos.y < 0 or self.pos.x > d.SCREEN_SIZE or self.pos.x < 0:
            self.die()

    def die(self):
        self.dead = True