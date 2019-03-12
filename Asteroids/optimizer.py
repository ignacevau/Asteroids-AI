import data as d
import random
import math
from neural_net import NeuralNetWork
import main
import copy
from spaceship import Spaceship
from utility import clamp, Vector2


def evolve():
    """ Generate a new population based on the result of the earlier one """
    d.next_gen = []

    """ Keep the best ship """
    net = copy.deepcopy(d.best_ship.neural_net)
    d.next_gen.append(Spaceship(net))

    """ Make low mutations from the best ship """
    for _ in range(d.BEST_SHIP_LOW_MUT):
        net = copy.deepcopy(d.best_ship.neural_net)
        net = mutate(net, False)
        d.next_gen.append(Spaceship(net))

    """ Make strong mutations from the best ship """
    for _ in range(d.BEST_SHIP_HIGH_MUT):
        net = copy.deepcopy(d.best_ship.neural_net)
        net = mutate(net, True)
        d.next_gen.append(Spaceship(net))

    """ Make mutations from the shitty ships """
    for i in range(d.SHITTY_SHIP_COUNT):
        ship = d.dead_ships[i]
        net = copy.deepcopy(ship.neural_net)
        net = mutate(net, True)
        d.next_gen.append(Spaceship(net))

    """ Make a few randoms """
    for _ in range(d.RANDOM_SHIP_COUNT):
        # A new instance of a NN is always random
        net = NeuralNetWork(d.INPUT_COUNT, d.HIDDEN_LAYERS, 1)
        d.next_gen.append(Spaceship(net))

    """ Cross-Breed fit ships and bad ships """
    children_fb = []
    breed_count = d.FIT_BAD_BREED_COUNT

    # Collect the fittest ships (died last)
    e_idx = len(d.dead_ships)-1
    fittest_ships = [d.dead_ships[e_idx-i] for i in range(d.FITTEST_SHIP_COUNT)]

    # Collect the worst ships (died first)
    worst_ships = [d.dead_ships[i] for i in range(d.WORST_SHIP_COUNT)]

    # Breed the fit and the bad ships
    for _ in range(breed_count):
        mom = fittest_ships[random.randint(0, len(fittest_ships)-1)]
        dad = worst_ships[random.randint(0, len(worst_ships)-1)]
        
        net = breed(mom.neural_net, dad.neural_net)
        children_fb.append(net)

    # Add the children to the population
    for i in range(len(children_fb)):
        d.next_gen.append(Spaceship(children_fb[i]))

    """ Cross-Breed rest of the population from the fittest ships """
    children_ff = []
    breed_count = d.POPULATION_COUNT - len(d.next_gen)

    # Collect the fittest ships
    fittest_ships = [d.dead_ships[len(d.dead_ships)-1-i] for i in range(d.FITTEST_SHIP_COUNT)]

    for _ in range(breed_count):
        # Find parents
        mom = fittest_ships[random.randint(0, len(fittest_ships)-1)]
        dad = mom
        # Make sure the two parent are different
        while dad == mom:
            dad = fittest_ships[random.randint(0, len(fittest_ships)-1)] 

        # Make children
        net = breed(mom.neural_net, dad.neural_net)
        children_ff.append(net)

   # Make strong mutations of 1/4 of the crossed children
    for i in range(int(len(children_ff)/4)):
        children_ff[i] = mutate(children_ff[i], True)

    # Make small mutations of 2/4 of the crossed children
    for i in range( int(len(children_ff)/4), int(len(children_ff)/4)*3 ):
        children_ff[i] = mutate(children_ff[i], False)

    # Add the children to the population
    for i in range(len(children_ff)):
        d.next_gen.append(Spaceship(children_ff[i]))

    """ Start a new simulation with the new population """
    d.main.reset()


def breed(mom, dad):
    """ Breed two neural networks """
    child = NeuralNetWork(d.INPUT_COUNT, d.HIDDEN_LAYERS, 1)

    """ weights """
    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            for k in range(len(child.weights[i][j])):
                # Every weight of the child is a random value between
                # the corresponding weight of its mom and dad
                child.weights[i][j][k] = random.uniform(mom.weights[i][j][k], dad.weights[i][j][k])
    
    """ biases """
    for i in range(len(child.biases)):
        if d.sensor_mode:
            # Bias is a number
            child.biases[i] = random.uniform(mom.biases[i], dad.biases[i])
        else:
            # Bias is a vector
            child.biases[i] = random.uniform(mom.biases[i], dad.biases[i])            

    return child


def mutate(net, strong):
    """ Mutate a neural network\n
        Parameters: \n
        \tnet = the neural net to mutate
        \tstrong = whether or not the mutation should be strong"""
    b = net.biases
    w = net.weights

    """ weights """
    w_new = net.weights
    for _ in range(d.MUTATED_WEIGHTS_COUNT):
        # Find a random weight
        layer_i = random.randint(0, len(w)-1)
        input_i = random.randint(0, len(w[layer_i])-1)
        weigth_i = random.randint(0, len(w[layer_i][input_i])-1)
        _w = w[layer_i][input_i][weigth_i]

        # How strong should the weight be mutated
        if(strong):
            mut_strength = d.MUTATION_STRENGTH_HIGH
        else:
            mut_strength = d.MUTATION_STRENGTH_LOW

        # Mutate the weight (weights are always clamped between -1 and 1)
        rd = random.uniform(-mut_strength, mut_strength)
        w_new[layer_i][input_i][weigth_i] = clamp(-1, 1, _w + rd * _w)

    net.weights = w_new

    """ biases """
    # Find a random bias
    index = random.randint(0, len(b)-1)

    # How strong should the bias be mutated
    rd = random.uniform(-mut_strength, mut_strength)

    # Mutate the bias
    if d.sensor_mode:
        # Bias is a number
        b[index] += rd
    else:
        # Bias is a vector
        b[index] += Vector2(rd, rd)
    
    net.biases = b

    return net