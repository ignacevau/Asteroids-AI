import data as d
import pygame as pg
from utility import Vector2
from spaceship import Spaceship
from asteroid import Asteroid
import random

class Main:
    def __init__(self):
        self.run = True
        self.spaceship = Spaceship()
        d.asteroids = [Asteroid(random.randint(1, 4))] * 4

    def draw(self):
        d.SURFACE.fill(d.BLACK)
        self.spaceship.draw()
        [asteroid.draw() for asteroid in d.asteroids]
        pg.display.update()

    def update(self):
        self.check_dead_player()
        self.check_dead_ast()
        self.spaceship.update()
        [asteroid.update() for asteroid in d.asteroids]

    def main(self):
        d.SURFACE = pg.display.set_mode((d.SCREEN_SIZE, d.SCREEN_SIZE))
        d.CLOCK = pg.time.Clock()
        
        while self.run:
            d.CLOCK.tick(60)
            self.update()
            self.draw()

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                pg.quit()
            if keys[pg.K_LEFT]:
                self.spaceship.turn(-1)
            if keys[pg.K_RIGHT]:
                self.spaceship.turn(1)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

    def new_asteroid(self):
        p = []
        if self.spaceship.pos.x > d.SCREEN_SIZE/2:
            p.append(2)
        else:
            p.append(4)
        if self.spaceship.pos.y > d.SCREEN_SIZE/2:
            p.append(3)
        else:
            p.append(1)
        return Asteroid(random.choice(p))

    def check_dead_ast(self):
        for i in range(len(d.asteroids)):
            if d.asteroids[i].dead:
                d.asteroids[i] = self.new_asteroid()

    def check_dead_player(self):
        if self.spaceship.dead:
            self.restart()

    def restart(self):
        self.spaceship.reset()
        d.asteroids = [Asteroid(i) for i in range(1, 5)]