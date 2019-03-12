import data as d
from utility import Vector2
import pygame as pg
import random
import math
import main

class Asteroid:
    """ Asteroids fly around killing spaceships\n
        Parameters:
        \tspawn_edge : (1, 2, 3, 4) = (top, right, bottom, left)"""

    def __init__(self, spawn_edge):
        self.dir = Vector2(0, 1)
        self.pos = Vector2()
        self.rad = random.randint(d.AST_MIN_SIZE, d.AST_MAX_SIZE)
        self.speed = random.uniform(d.AST_MIN_SPD, d.AST_MAX_SPD)
        self.dead = False
        self.color = d.WHITE

        self.spawn(spawn_edge)


    def spawn(self, edge):
        """ Spawn the asteroid at the given edge """
        s = d.SCREEN_SIZE
        rd = random.uniform(0, s)

        # Get the position
        if edge == 1:
            self.pos.x = rd
            self.pos.y = 0
            self.dir = Vector2(0, 1)
        elif edge == 2:
            self.pos.x = s
            self.pos.y = rd
            self.dir = Vector2(-1, 0)
        elif edge == 3:
            self.pos.x = rd
            self.pos.y = s
            self.dir = Vector2(0, -1)
        else:
            self.pos.x = 0
            self.pos.y = rd
            self.dir = Vector2(1, 0)

        # Choose random direction (towards the center direction)
        self.dir.rotate(random.uniform(-math.pi/2, math.pi/2), Vector2())        


    def draw(self):
        """ Draw the asteroid """
        pg.draw.circle(d.SURFACE, self.color, self.pos.tupled(), self.rad, 1)


    def update(self):
        """ Update the asteroid """
        # Update position
        self.pos += self.dir * self.speed

        # Check whether asteroid leaves the screen
        self.check_boundaries()


    def check_boundaries(self):
        """ Check whether the asteroid leaves the screen """
        if self.pos.y > d.SCREEN_SIZE:      # Leaves bottom side
            self.pos.y = 0
        elif self.pos.y < 0:                # Leaves top side
            self.pos.y = d.SCREEN_SIZE

        if self.pos.x > d.SCREEN_SIZE:      # Leaves right side
            self.pos.x = 0
        elif self.pos.x < 0:                # Leaves left side
            self.pos.x = d.SCREEN_SIZE


    def die(self):
        """ Kill the asteroid """
        self.dead = True

        # Replace the dead asteroid with a new one
        main.check_dead_ast()