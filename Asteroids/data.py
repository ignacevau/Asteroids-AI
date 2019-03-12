""" General settings """
solo = False             # Play it yourself
sensor_mode = True       # Ships see through sensors instead of asteroid positions         


""" Colors """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 61, 70)
NEON_BLUE = (0, 255, 178)


""" Asteroid settings """
asteroids = []      # List containing all the current asteroids
AST_MIN_SPD = 2     # Minimum speed
AST_MAX_SPD = 5     # Maximum speed
AST_MIN_SIZE = 25
AST_MAX_SIZE = 50
AST_COUNT = 5       # Amount of asteroids on the screen

# How many of the closest asteroids should be used for inputs
CLOSEST_AST_COUNT = 3


""" Player settings """
PLAYER_W = 20       # Player's width
PLAYER_H = 30       # Player's height
SPEED = 10
TURN_SPEED = 10

# Sensor settings (if sensors are used!)
SENSOR_LENGTH = 300     # Length of the sensors
SENSOR_COUNT = 15       # Amount of sensors

MAX_ROTATION_TRESHOLD = 0.4         # Max amount of circles the ship can make
                                    # Prevent ships from only spinning around (sensor mode only)    
CHECK_ROT_TIME = 1000               # Milliseconds from the start in which the ship can't make more
                                    # circles than the treshold


""" Text components """
FONT = None
TXT_GEN_RDR = None
TXT_GEN = ""
TXT_ALIVE_RDR = None
TXT_ALIVE = ""
TXT_DEAD_RDR = None
TXT_DEAD = ""


""" Neural network settings """
# Amount of input neurons (fixed!)
INPUT_COUNT = SENSOR_COUNT if sensor_mode else CLOSEST_AST_COUNT

# Hidden layer construction:
#  - Every new integer represents a new hidden layer
#  - with the integer being the amount of neurons
HIDDEN_LAYERS = [7,2]


""" Population optimizer settings """
next_gen = []       # List with next population

POPULATION_COUNT = 100      # Total amount of ships per population

FITTEST_SHIP_COUNT = 15     # Amount of fittest ships used to breed
WORST_SHIP_COUNT = 10       # Amount of worst ships used to breed

# Population structure
RANDOM_SHIP_COUNT = 5       # Amount random ships
SHITTY_SHIP_COUNT = 5       # Amount (high) mutations from the shitty ships (WORST_SHIP_COUNT)
BEST_SHIP_HIGH_MUT = 10     # Amount (high) mutations from the best ship
BEST_SHIP_LOW_MUT = 30      # Amount (low) mutations from the best ship
FIT_BAD_BREED_COUNT = 10    # Amount breeds between worst and fittest ships
# The rest of the population will be filled
# with breeds between the fittest ships (FITTEST_SHIP_COUNT)

# Weight settings
MUTATED_WEIGHTS_COUNT = 30      # Amount of weights to be mutated (single ship)
# (Percentages of the original weight value)
MUTATION_STRENGTH_HIGH = 0.3    # Mutation strength for high mutations
MUTATION_STRENGTH_LOW = 0.1     # Mutation strength for low mutations


""" Pygame variables """
main = None
SURFACE = None
SCREEN_SIZE = 800
CLOCK = None


# In-game updated variables
paused = False
spaceships = []
dead_ships = []
alive_ships = []
best_ship = None
generation = 0