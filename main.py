#!/usr/bin/env python3
"""Main entry point for TSP GA solver.

Author: Guglielmo Cimolai
Date: 30/06/2025
Version: v2
"""

import time
from core.cities import generate_cities
from core.distance import calculate_distance_matrix
from algorithms.sga import StandardGA
import config


def get_adaptive_parameters(num_cities):
    """Get parameters adapted to problem size.

    Args:
        num_cities: Number of cities in the problem

    Returns:
        dict: Dictionary of SGA parameters
    """
    params = {
        "population_size": config.DEFAULT_SGA_POP_SIZE,
        "generations": config.DEFAULT_SGA_GENERATIONS,
        "crossover_rate": config.DEFAULT_SGA_CROSSOVER_RATE,
        "mutation_rate": config.DEFAULT_SGA_MUTATION_RATE,
        "elitism_size": config.DEFAULT_SGA_ELITISM_SIZE,
        "tournament_size": config.DEFAULT_SGA_TOURNAMENT_K
    }

    # Adapt parameters based on problem size
    if num_cities <= 50:
        params.update({
            "generations": 750,
            "population_size": 100
        })
    elif num_cities <= 100:
        params.update({
            "generations": 1500,
            "population_size": 200,
            "elitism_size": 10
        })
    else:
        params.update({
            "generations": 5000,
            "population_size": 200,
            "elitism_size": 15
        })

    return params


def main():
    """Run TSP solver with configured parameters."""
    # Generate cities
    cities = generate_cities(
        config.NUM_CITIES,
        width=config.CITY_WIDTH,
        height=config.CITY_HEIGHT,
        seed=config.CITY_SEED
    )

    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(cities)
    print(f"Generated {config.NUM_CITIES} cities. Distance matrix calculated.")

    # Get adaptive parameters
    sga_params = get_adaptive_parameters(config.NUM_CITIES)

    # Print parameters
    print(f"\nSGA Parameters: {sga_params}")

    # Create and run SGA
    sga = StandardGA(cities, distance_matrix)

    # Time the execution
    start_time = time.time()
    best_individual = sga.solve(**sga_params)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"SGA execution time: {execution_time:.2f} seconds")

    # Print final results
    print("\n" + "=" * 20 + " Final Results " + "=" * 20)
    print(f"Problem: {config.NUM_CITIES} cities (Seed: {config.CITY_SEED})")
    print(f"\nStandard GA (SGA):")
    print(f"  Best Cost: {best_individual.cost:.2f}")
    print(f"  Best Tour: {best_individual.tour}")
    print(f"  Execution Time: {execution_time:.2f}s")
    print("\nSGA execution finished.")


if __name__ == "__main__":
    main()
