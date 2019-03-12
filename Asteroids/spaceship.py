import data as d
from utility import Vector2, Algs
import pygame as pg
import math
import numpy as np
from neural_net import NeuralNetWork
import main

class Spaceship:
    def __init__(self, neural_net):
        self.pos = Vector2(d.SCREEN_SIZE/2, d.SCREEN_SIZE/2)
        self.points = [Vector2()]*3 # Shape points of the player (triangle)
        self.dir = Vector2(0, -1)   # Direction in which the ship moves
        self.rotation = 0           # Rotation of the ship (radians)
        self.dead = False

        # Inputs fed to the neural network:
        # If sensor mode: the length of each sensor
        # Else: the distance vectors to the closest asteroids
        self.inputs = [] * d.INPUT_COUNT

        if d.sensor_mode:
            # Configure the ship's sensors
            self.sensors = []
            self.setup_sensors()
        else:
            # Indices of the asteroids closest to the player
            # of 'data.asteroids' list
            self.ast_idx = [0] * d.CLOSEST_AST_COUNT

        self.neural_net = neural_net
        self.start_time = pg.time.get_ticks()
        self.speed = d.SPEED
        self.color = d.NEON_BLUE

    def setup_sensors(self):
        """ Setup the sensors of the spaceship """
        self.sensors = []
        for i in range(d.SENSOR_COUNT):
            # Angles in degrees
            offset = 90
            angle = (180 / (d.SENSOR_COUNT-1)) * i - offset

            self.sensors.append(Sensor(angle))

    def draw(self):
        """ Draw the spaceship """
        if self.dead:
            return

        # Collect the positions of the player's shape points
        tupled_points = []
        for point in self.points:
            tupled_points.append(point.tupled())

        # Draw the player
        pg.draw.aalines(d.SURFACE, self.color, True, tupled_points, 2)
        
        if d.sensor_mode:
            # Draw the sensors of the player
            [sensor.draw(d.WHITE, 1) for sensor in self.sensors]

    def update(self):
        """ Update the spaceship """
        if self.dead:
            return

        if d.sensor_mode:
            # Update the sensor distances
            [sensor.update(self.dir, self.pos) for sensor in self.sensors]
            
            # Check whether a ship keeps spinning around in the middle
            self.check_crazy_rotation()
        else:
            self.get_closest_ast()

        self.update_inputs()        
        
        self.pos += self.dir * self.speed
        if not d.solo:
            self.turn(self.neural_net.forward_prop(self.inputs))

        self.check_boundaries()
        self.check_collision()
        self.update_points_pos()
        

    def check_crazy_rotation(self):
        """ Check whether a ship keeps spinning around in the middle """
        if self.start_time != None:
            if self.start_time < pg.time.get_ticks() - d.CHECK_ROT_TIME:
                if math.fabs(self.rotation) > (2*math.pi) * d.MAX_ROTATION_TRESHOLD:  # 2*pi = 1 full circle
                    self.die()
                else:
                    self.start_time = None


    def update_points_pos(self):
        """ Update the position of the shape points of the ship (triangle) """
        half_h = d.PLAYER_H / 2
        half_w = d.PLAYER_W / 2

        # Top point
        self.points[0] = self.pos + self.dir * half_h
        # Right point
        self.points[1] = self.pos + self.dir.get_perpd() * half_w - self.dir * half_h
        # Left point
        self.points[2] = self.pos - self.dir.get_perpd() * half_w - self.dir * half_h


    def turn(self, out):
        """ Control the spaceship's direction through neural network output or key input """
        if not d.solo:
            if d.sensor_mode:
                angle = out - 0.5
                angle *= d.TURN_SPEED
                self.rotation -= angle
                self.dir.rotate(-angle, Vector2())
            else:
                # x and y are between (0, 1) --> (-0.5, 0.5)
                out.x -= 0.5
                out.y -= 0.5

                out = out.normalized()

                # Turn the spaceship by changing its direction
                r = self.dir + out
                self.dir = (self.dir + r.normalized()*d.TURN_SPEED).normalized()
        else:
            angle = out - 0.5
            angle *= 0.2
            self.rotation -= angle
            self.dir.rotate(-angle, Vector2())


    def check_boundaries(self):
        """ Check whether the spaceship leaves the screen """
        if self.pos.y > d.SCREEN_SIZE:      # Leaves bottom side
            self.pos.y = 0
        elif self.pos.y < 0:                # Leaves top side
            self.pos.y = d.SCREEN_SIZE

        if self.pos.x > d.SCREEN_SIZE:      # Leaves right side
            self.pos.x = 0
        elif self.pos.x < 0:                # Leaves left side
            self.pos.x = d.SCREEN_SIZE


    def check_collision(self):
        """ Check for collisions with asteroids """
        for a in d.asteroids:
            # Check for every side of the ship
            for i in range(len(self.points)):
                j = i+1
                if(i == len(self.points)-1):
                    j = 0

                x1 = self.points[i].x
                y1 = self.points[i].y
                x2 = self.points[j].x
                y2 = self.points[j].y

                # Calculate the distance
                l = Algs.get_distance_to_segment(a.pos.x, a.pos.y, x1, y1, x2, y2)
                if l - a.rad <= 0:
                    self.die()


    def get_closest_ast(self):
        """ Find the closest asteroids to the spaceship """
        ds = []
        for ast in d.asteroids:
            distance = Algs.get_distance(self.pos, ast.pos) - ast.rad
            ds.append(distance)
        a = np.array(ds)
        
        # Get indices of the closest asteroids
        self.ast_idx = np.argpartition(a, -d.CLOSEST_AST_COUNT)[:d.CLOSEST_AST_COUNT].tolist()


    def update_inputs(self):
        """ Update the ship's inputs used for the neural network """
        self.inputs = []
        if d.sensor_mode:
            # Inputs are the distances of the sensors
            for sensor in self.sensors:
                input = sensor.dist / d.SENSOR_LENGTH       # Scale the inputs between 0 and 1
                self.inputs.append(input)
        else:
            # Inputs are the distance vectors of the closest asteroids
            for index in self.ast_idx:
                a_p = d.asteroids[index].pos - self.pos
                n = a_p.normalized()

                dist = []
                d1 = a_p

                # Find all the possible distances to the spaceship for the current asteroid
                # For example when the player is far right and the asteroid far left,
                # the player is still close to the asteroid (through the screen)
                dist.append(d1 - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 - Vector2(d.SCREEN_SIZE, 0)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 + Vector2(d.SCREEN_SIZE, 0)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 - Vector2(0, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 + Vector2(0, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 - Vector2(d.SCREEN_SIZE, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 + Vector2(d.SCREEN_SIZE, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 - Vector2(-d.SCREEN_SIZE, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))
                dist.append((d1 + Vector2(-d.SCREEN_SIZE, d.SCREEN_SIZE)) - n*(d.asteroids[index].rad + d.PLAYER_H))

                # Take the smallest distance
                m = Algs.v2_min(dist)
                m.x = m.x
                m.y = m.y
                self.inputs.append(m)


    def die(self):
        """ Kill the spaceship """
        if(self.dead):
            return

        if d.solo:
            d.main.reset()
        else:
            self.dead = True
            d.main.update_text()

            d.dead_ships.append(self)
            d.alive_ships.remove(self)

            if len(d.dead_ships) == d.POPULATION_COUNT:
                d.generation += 1

                # Assign the last ship alive as the best ship
                d.best_ship = d.dead_ships[len(d.dead_ships)-1]

                # Reload the population
                main.reload()
        

    def reset(self):
        """ Reset the spaceship """
        self.dead = False
        self.pos = Vector2(d.SCREEN_SIZE/2, d.SCREEN_SIZE/2)
        self.velocity = Vector2()
        self.angular_vel = 0
        self.rotation = 0


class Sensor:
    """ Sensor with which the player sees in a locked direction\n
        Parameters: \n
        \tangle = Angle of the sensor in respect to the player (degrees)"""
    def __init__(self, angle):
        self.angle = angle              # In degrees
        self.dir = Vector2()
        self.pos = Vector2()            # Start position (= Ship position)
        self.end_pos = Vector2()        # End of the sensor
        self.ship_dir = Vector2()
        self.inters = None              # Intersection point
        self.dist = d.SENSOR_LENGTH     # Length of the sensor


    def update(self, ship_dir, ship_pos):
        """ Update the sensor\n
            Parameters:
            \tship_dir = direction vector of the ship
            \tship_pos = position vector of the ship """
        self.ship_dir = ship_dir
        self.dir = ship_dir.rotated(self.angle)
        self.pos = ship_pos
        self.end_pos = self.pos + self.dir * d.SENSOR_LENGTH
        self.get_ast_collision()


    def draw(self, color, width):
        """ Draw the sensor """
        if self.inters != None:
            # There is an intersection
            # Draw the intersection point
            pg.draw.circle(d.SURFACE, color, self.inters.tupled(), 4)
            # Intersection --> shorter ray length
            pg.draw.line(d.SURFACE, color, self.pos.tupled(), self.inters.tupled(), width)
        else:
            # No intersection --> full sensor length
            pg.draw.line(d.SURFACE, color, self.pos.tupled(), self.end_pos.tupled(), width)


    def get_ast_collision(self):
        """ Find instersection with asteroids """
        self.inters = None
        self.dist = d.SENSOR_LENGTH

        for i in range(len(d.asteroids)):
            a = d.asteroids[i]
            # Get the intersection point of the sensor segment and the asteroid
            s = Algs.get_segment_circle_inters(self.pos, self.end_pos, a.pos, a.rad)

            # There is an intersection
            if s != None:
                # First intersection with asteroid
                if self.inters == None:
                    self.inters = s
                    self.dist = Algs.get_distance(self.pos, self.inters)
                else:
                    # Intersection with multiple asteroids
                    # Assign the smallest distance
                    new_dist = Algs.get_distance(self.pos, s)
                    if new_dist < self.dist:
                        self.inters = s
                        self.dist = new_dist
