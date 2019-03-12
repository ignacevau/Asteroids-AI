import data as d
import pygame as pg
from utility import Vector2
from spaceship import Spaceship
from asteroid import Asteroid
import random
from neural_net import NeuralNetWork
import optimizer
import os

def check_dead_ast():
    """ Replace the dead asteroids with new ones """
    if len(d.alive_ships) > 0:
        # Check whether there are still ships alive
        for i in range(len(d.asteroids)):
            if d.asteroids[i].dead:
                d.asteroids[i] = new_asteroid()

def new_asteroid():
    """ Spawn a new asteroid """
    pos = []
    if d.alive_ships[0].pos.x > d.SCREEN_SIZE/2:    # Ship is on the right half
        pos.append(2)
    else:                                           # Ship is on the left half
        pos.append(4)

    if d.alive_ships[0].pos.y > d.SCREEN_SIZE/2:    # Ship is the bottom half
        pos.append(3)
    else:                                           # Ship is on the top half
        pos.append(1)

    # Return a random asteroid not on the player's position
    return Asteroid(random.choice(pos))

def reload():
    """ Start the new generation """
    optimizer.evolve()


class Main:
    """ The main class that controls everything """
    def __init__(self):
        pg.init()

        if os.path.exists('ExoFont.otf'):
            d.FONT = pg.font.Font("ExoFont.otf", 18)
        else:
            d.FONT = pg.font.Font(None, 18)

        if not d.solo:
            d.spaceships = [Spaceship(NeuralNetWork(d.INPUT_COUNT, d.HIDDEN_LAYERS, 1)) for _ in range(d.POPULATION_COUNT)]
            d.alive_ships = d.spaceships[:]
        else:
            self.spaceship = Spaceship(NeuralNetWork(d.INPUT_COUNT, d.HIDDEN_LAYERS, 1))
            d.alive_ships = [self.spaceship]

        # Setup asteroids
        d.asteroids = []
        for _ in range(d.AST_COUNT):
            d.asteroids.append(Asteroid(random.randint(1, 4)))

        self.update_text()


    def update(self):
        """ Update all the active objects """
        if not d.solo:
            [spaceship.update() for spaceship in d.spaceships]
        [asteroid.update() for asteroid in d.asteroids]

        if d.solo:
            self.spaceship.update()


    def update_text(self):
        """ Update the text on the screen """
        d.TXT_GEN = "Gen : %s" %(d.generation)
        d.TXT_GEN_RDR = d.FONT.render(d.TXT_GEN, 0, d.WHITE)
        d.TXT_ALIVE = "Alive : %s" %(len(d.alive_ships))
        d.TXT_ALIVE_RDR = d.FONT.render(d.TXT_ALIVE, 0, d.WHITE)
        d.TXT_DEAD = "Dead : %s" %(len(d.dead_ships))
        d.TXT_DEAD_RDR = d.FONT.render(d.TXT_DEAD, 0, d.WHITE)


    def draw(self):
        """ Draw all the active objects on the screen """
        d.SURFACE.fill(d.BLACK)
        if not d.solo:
            [spaceship.draw() for spaceship in d.spaceships]
        [asteroid.draw() for asteroid in d.asteroids]

        if d.solo:
            self.spaceship.draw()
        self.draw_text()
        pg.display.update()


    def draw_text(self):
        """ Draw the text on the screen """
        d.SURFACE.blit(d.TXT_GEN_RDR, (50, 20))
        d.SURFACE.blit(d.TXT_ALIVE_RDR, (50, 40))
        d.SURFACE.blit(d.TXT_DEAD_RDR, (50, 50))


    def reset(self):
        """ Reset the population and asteroids """
        if d.solo:
            # Only reset the player
            self.spaceship = Spaceship(NeuralNetWork(d.INPUT_COUNT, d.HIDDEN_LAYERS, 1))
            d.alive_ships = [self.spaceship]
        else:
            # Load the new generation
            d.best_ship = None
            d.spaceships = d.next_gen
            d.alive_ships = d.spaceships
            d.dead_ships = []

        # Reset the asteroids
        d.asteroids = []
        for _ in range(d.AST_COUNT):
            d.asteroids.append(Asteroid(random.randint(1, 4)))


    def main(self):
        """ Main loop """
        d.SURFACE = pg.display.set_mode((d.SCREEN_SIZE, d.SCREEN_SIZE))
        d.CLOCK = pg.time.Clock()
        
        # In what stage the space_key press is
        space_stage = 0

        while True:
            d.CLOCK.tick(60)

            if not d.paused:
                self.update()
            self.draw()

            keys = pg.key.get_pressed()

            # Player controls
            if d.solo:
                if keys[pg.K_LEFT]:
                    self.spaceship.turn(0)
                if keys[pg.K_RIGHT]:
                    self.spaceship.turn(1)

            # Space = pause
            if keys[pg.K_SPACE]:
                # Space is pressed
                if space_stage == 0:
                    d.paused = not d.paused
                    space_stage = 1

            # Esc = quit
            if keys[pg.K_ESCAPE]:
                pg.quit()

            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    # Space is not pressed anymore
                    if event.key == pg.K_SPACE:            
                        space_stage = 0
                if event.type == pg.QUIT:
                    pg.quit()