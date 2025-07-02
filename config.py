"""Configuration parameters for TSP GA."""

# Problem settings
NUM_CITIES = 50    # Number of cities
CITY_SEED = 1      # Seed for reproducible city generation
CITY_WIDTH = 100   # Grid width
CITY_HEIGHT = 100  # Grid height

# SGA parameters
DEFAULT_SGA_POP_SIZE = 100         # Population size
DEFAULT_SGA_GENERATIONS = 1000     # Number of generations
DEFAULT_SGA_CROSSOVER_RATE = 0.85  # Crossover rate
DEFAULT_SGA_MUTATION_RATE = 0.15   # Mutation rate
DEFAULT_SGA_ELITISM_SIZE = 5       # Elitism size
DEFAULT_SGA_TOURNAMENT_K = 3       # Tournament size

# HGA-ACO parameters
DEFAULT_HGA_POP_SIZE = 100
DEFAULT_HGA_GENERATIONS = 250
DEFAULT_HGA_GA_CROSSOVER_RATE = 0.7      # Crossover rate for GA portion
DEFAULT_HGA_ACO_CONTRIBUTION_RATE = 0.5  # Proportion of ACO individuals
DEFAULT_HGA_MUTATION_RATE = 0.15
DEFAULT_HGA_ELITISM_SIZE = 5
DEFAULT_HGA_TOURNAMENT_K = 3

# ACO-specific parameters
DEFAULT_HGA_ALPHA = 1.0             # Pheromone influence
DEFAULT_HGA_BETA = 3.0              # Heuristic (distance) influence
DEFAULT_HGA_EVAPORATION_RATE = 0.3  # Pheromone evaporation rate (rho)
DEFAULT_HGA_Q_PHEROMONE = 100.0     # Pheromone deposit constant
DEFAULT_HGA_INITIAL_PHEROMONE = 0.1
DEFAULT_HGA_BEST_N_DEPOSIT = 5      # Number of best individuals to deposit pheromones

# Visualization settings
LIVE_PLOT_UPDATE_FREQ = 1  # Update plot every N generations (0 to disable)

# Display settings
VERBOSE = True
PROGRESS_FREQUENCY = 10  # Print progress every N generations
