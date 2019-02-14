from utility import Vector2

SURFACE = None
SCREEN_SIZE = 800
CLOCK = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 61, 70)
NEON_BLUE = (0, 255, 178)

# Spawn area parameters of asteroids
asteroids = []
AST_MIN_SPD = 1.5
AST_MAX_SPD = 3.5
AST_MIN_SIZE = 15
AST_MAX_SIZE = 35

PLAYER_W = 30
PLAYER_H = 40

# Don't change parameters if not necessairy!
SPEED = 0.8
TURN_SPEED = 4
ANG_DRAG = 0.94
DRAG = 0.95
POWER = 0.5

CLOSEST_AST_COUNT = 3

HIDDEN_LAYERS = [5]

MUTATED_WEIGHTS_COUNT = 40
MUTATION_STRENGTH = 0.5