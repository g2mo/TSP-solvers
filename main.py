#!/usr/bin/env python3
"""Main entry point for TSP GA solver.

Author: Guglielmo Cimolai
Date: 30/06/2025
"""

from core.cities import get_fixed_cities
from core.distance import calculate_distance_matrix
from algorithms.sga import StandardGA
import config


def main():
    """Run TSP solver with configured parameters."""
    # Get cities
    cities = get_fixed_cities()
    num_cities = len(cities)

    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(cities)
    print(f"Problem: {num_cities} fixed cities. Distance matrix calculated.")

    # Create and run SGA
    sga = StandardGA(cities, distance_matrix)
    best_individual = sga.solve(
        population_size=config.POP_SIZE,
        generations=config.GENERATIONS,
        crossover_rate=config.CROSSOVER_RATE,
        mutation_rate=config.MUTATION_RATE,
        tournament_size=config.TOURNAMENT_K
    )

    # Print final results
    print("\n" + "=" * 10 + " SGA Run Complete " + "=" * 10)
    print(f"Final Best Individual found:")
    print(f"  Cost: {best_individual.cost:.2f}")
    print(f"  Tour: {best_individual.tour}")
    print("Execution finished.")


if __name__ == "__main__":
    main()
