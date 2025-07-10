"""Configuration parameters for TSP GA."""

# Algorithm selection toggles
ENABLE_SGA = True  # Standard Genetic Algorithm
ENABLE_HGA_ACO = True  # Hybrid GA-ACO
ENABLE_PSO = True  # Particle Swarm Optimization

# Problem settings
NUM_CITIES = 50  # Number of cities (determines parameter preset: <50, 50-100, >100)
CITY_SEED = 1  # Seed for reproducible city generation
CITY_WIDTH = 100  # Grid width
CITY_HEIGHT = 100  # Grid height

# Display settings
VERBOSE = True
PROGRESS_FREQUENCY = 10

# Dynamic TSP settings
ENABLE_DYNAMIC_TSP = True  # Enable dynamic moving cities
DYNAMIC_MOVEMENT_SEED = 1  # Seed for reproducible city movements

# ======================================================================
# PARAMETER PRESETS FOR DIFFERENT PROBLEM SIZES
# ======================================================================
# The system automatically selects parameters based on NUM_CITIES:
# - Small:  < 50 cities   → Fast execution, good for testing
# - Medium: 50-100 cities → Balanced performance
# - Large:  > 100 cities  → Maximum solution quality
# ======================================================================

# Small problems (< 50 cities)
SMALL_PROBLEM_PARAMS = {
    # SGA parameters
    "SGA_POP_SIZE": 100,
    "SGA_GENERATIONS": 750,
    "SGA_CROSSOVER_RATE": 0.85,
    "SGA_MUTATION_RATE": 0.15,
    "SGA_ELITISM_SIZE": 5,
    "SGA_TOURNAMENT_K": 3,

    # HGA-ACO parameters
    "HGA_POP_SIZE": 50,
    "HGA_GENERATIONS": 250,
    "HGA_GA_CROSSOVER_RATE": 0.7,
    "HGA_ACO_CONTRIBUTION_RATE": 0.5,
    "HGA_MUTATION_RATE": 0.15,
    "HGA_ELITISM_SIZE": 5,
    "HGA_TOURNAMENT_K": 3,
    "HGA_ALPHA": 1.0,
    "HGA_BETA": 3.0,
    "HGA_EVAPORATION_RATE": 0.3,
    "HGA_Q_PHEROMONE": 100.0,
    "HGA_INITIAL_PHEROMONE": 0.1,
    "HGA_BEST_N_DEPOSIT": 3,

    # PSO parameters
    "PSO_NUM_PARTICLES": 15,
    "PSO_GENERATIONS": 250,
    "PSO_W": 0.4,
    "PSO_C1": 2.0,
    "PSO_C2": 2.0,
    "PSO_USE_LOCAL_SEARCH": True,

    # Visualization
    "LIVE_PLOT_UPDATE_FREQ": 1
}

# Medium problems (50-100 cities)
MEDIUM_PROBLEM_PARAMS = {
    # SGA parameters
    "SGA_POP_SIZE": 100,
    "SGA_GENERATIONS": 1500,
    "SGA_CROSSOVER_RATE": 0.85,
    "SGA_MUTATION_RATE": 0.15,
    "SGA_ELITISM_SIZE": 10,
    "SGA_TOURNAMENT_K": 3,

    # HGA-ACO parameters
    "HGA_POP_SIZE": 100,
    "HGA_GENERATIONS": 500,
    "HGA_GA_CROSSOVER_RATE": 0.7,
    "HGA_ACO_CONTRIBUTION_RATE": 0.5,
    "HGA_MUTATION_RATE": 0.15,
    "HGA_ELITISM_SIZE": 5,
    "HGA_TOURNAMENT_K": 3,
    "HGA_ALPHA": 1.0,
    "HGA_BETA": 3.0,
    "HGA_EVAPORATION_RATE": 0.3,
    "HGA_Q_PHEROMONE": 100.0,
    "HGA_INITIAL_PHEROMONE": 0.1,
    "HGA_BEST_N_DEPOSIT": 5,

    # PSO parameters
    "PSO_NUM_PARTICLES": 25,
    "PSO_GENERATIONS": 500,
    "PSO_W": 0.5,
    "PSO_C1": 2.0,
    "PSO_C2": 2.0,
    "PSO_USE_LOCAL_SEARCH": True,

    # Visualization
    "LIVE_PLOT_UPDATE_FREQ": 5
}

# Large problems (> 100 cities)
LARGE_PROBLEM_PARAMS = {
    # SGA parameters
    "SGA_POP_SIZE": 200,
    "SGA_GENERATIONS": 5000,
    "SGA_CROSSOVER_RATE": 0.85,
    "SGA_MUTATION_RATE": 0.20,
    "SGA_ELITISM_SIZE": 15,
    "SGA_TOURNAMENT_K": 5,

    # HGA-ACO parameters
    "HGA_POP_SIZE": 200,
    "HGA_GENERATIONS": 1000,
    "HGA_GA_CROSSOVER_RATE": 0.65,
    "HGA_ACO_CONTRIBUTION_RATE": 0.6,
    "HGA_MUTATION_RATE": 0.20,
    "HGA_ELITISM_SIZE": 10,
    "HGA_TOURNAMENT_K": 5,
    "HGA_ALPHA": 1.2,
    "HGA_BETA": 2.5,
    "HGA_EVAPORATION_RATE": 0.4,
    "HGA_Q_PHEROMONE": 100.0,
    "HGA_INITIAL_PHEROMONE": 0.05,
    "HGA_BEST_N_DEPOSIT": 10,

    # PSO parameters
    "PSO_NUM_PARTICLES": 30,
    "PSO_GENERATIONS": 1000,
    "PSO_W": 0.6,
    "PSO_C1": 1.8,
    "PSO_C2": 2.2,
    "PSO_USE_LOCAL_SEARCH": True,

    # Visualization
    "LIVE_PLOT_UPDATE_FREQ": 10
}


# ======================================================================
# QUICK REFERENCE: KEY PARAMETERS BY PROBLEM SIZE
# ======================================================================
# Parameter         | Small (<50) | Medium (50-100) | Large (>100)
# ----------------- | ----------- | --------------- | ------------
# SGA Population    | 100         | 100             | 200
# SGA Generations   | 750         | 1500            | 5000
# HGA Population    | 50          | 100             | 200
# HGA Generations   | 250         | 500             | 1000
# PSO Particles     | 15          | 25              | 30
# PSO Generations   | 250         | 500             | 1000
# Plot Update Freq  | 1           | 5               | 10
# ======================================================================

# ==================================================
# FUNCTION TO GET APPROPRIATE PARAMETERS
# ==================================================

def get_problem_params(num_cities):
    """Get appropriate parameter set based on problem size.

    Args:
        num_cities: Number of cities in the problem

    Returns:
        dict: Parameter dictionary for the problem size
    """
    if num_cities < 50:
        return SMALL_PROBLEM_PARAMS
    elif num_cities <= 100:
        return MEDIUM_PROBLEM_PARAMS
    else:
        return LARGE_PROBLEM_PARAMS


# ==================================================
# CUSTOM PARAMETERS (Override presets here)
# ==================================================

# Set to None to use presets, or define custom parameters
CUSTOM_PARAMS = None

# Example custom parameters (uncomment and modify to use):
# CUSTOM_PARAMS = {
#     "SGA_POP_SIZE": 75,
#     "SGA_GENERATIONS": 250,
#     "SGA_CROSSOVER_RATE": 0.9,
#     "SGA_MUTATION_RATE": 0.1,
#     "SGA_ELITISM_SIZE": 3,
#     "SGA_TOURNAMENT_K": 4,
#     # ... add other parameters as needed
# }

# ==================================================
# EXAMPLE TEST CONFIGURATIONS
# ==================================================

# Quick test (10 cities, fast execution):
# NUM_CITIES = 10

# Standard benchmark (50 cities, balanced):
# NUM_CITIES = 50

# Challenge problem (150 cities, quality focus):
# NUM_CITIES = 150

# Compare only GA algorithms:
# ENABLE_SGA = True
# ENABLE_HGA_ACO = True
# ENABLE_PSO = False

# Test PSO vs HGA-ACO:
# ENABLE_SGA = False
# ENABLE_HGA_ACO = True
# ENABLE_PSO = True
