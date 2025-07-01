"""Configuration parameters for TSP GA."""

# Problem settings
NUM_CITIES = 50    # Number of cities
CITY_SEED = 1      # Seed for reproducible city generation
CITY_WIDTH = 100   # Grid width
CITY_HEIGHT = 100  # Grid height

# SGA parameters (defaults, can be overridden based on problem size)
DEFAULT_SGA_POP_SIZE = 100         # Population size
DEFAULT_SGA_GENERATIONS = 1000     # Number of generations
DEFAULT_SGA_CROSSOVER_RATE = 0.85  # Crossover rate
DEFAULT_SGA_MUTATION_RATE = 0.15   # Mutation rate
DEFAULT_SGA_ELITISM_SIZE = 5       # Elitism size
DEFAULT_SGA_TOURNAMENT_K = 3       # Tournament size

# Display settings
VERBOSE = True
PROGRESS_FREQUENCY = 10  # Print progress every N generations
