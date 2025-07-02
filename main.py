#!/usr/bin/env python3
"""Main entry point for TSP GA solver.

Author: Guglielmo Cimolai
Date: 2/07/2025
Version: v3
"""

import time
from core.cities import generate_cities
from core.distance import calculate_distance_matrix
from algorithms.sga import StandardGA
from visualization.plotter import TSPPlotterSGA
import config


def get_adaptive_parameters(num_cities):
    """Get parameters adapted to problem size.

    Args:
        num_cities: Number of cities in the problem

    Returns:
        tuple: (sga_params dict, plot_update_freq)
    """
    params = {
        "population_size": config.DEFAULT_SGA_POP_SIZE,
        "generations": config.DEFAULT_SGA_GENERATIONS,
        "crossover_rate": config.DEFAULT_SGA_CROSSOVER_RATE,
        "mutation_rate": config.DEFAULT_SGA_MUTATION_RATE,
        "elitism_size": config.DEFAULT_SGA_ELITISM_SIZE,
        "tournament_size": config.DEFAULT_SGA_TOURNAMENT_K
    }

    # Default plot frequency
    plot_freq = config.LIVE_PLOT_UPDATE_FREQ

    # Adapt parameters based on problem size
    if num_cities <= 50:
        params.update({
            "generations": 750,
            "population_size": 100
        })
        plot_freq = 1
    elif num_cities <= 100:
        params.update({
            "generations": 1500,
            "population_size": 200,
            "elitism_size": 10
        })
        plot_freq = 5
    else:
        params.update({
            "generations": 5000,
            "population_size": 250,
            "elitism_size": 15
        })
        plot_freq = 10

    return params, plot_freq


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
    sga_params, current_live_plot_freq = get_adaptive_parameters(config.NUM_CITIES)

    # Update global plot frequency
    config.LIVE_PLOT_UPDATE_FREQ = current_live_plot_freq

    # Warn about plotting performance for large problems
    if (config.NUM_CITIES > 100 and
            config.LIVE_PLOT_UPDATE_FREQ > 0 and
            config.LIVE_PLOT_UPDATE_FREQ < 10):
        print(f"INFO: Live plot update frequency is {config.LIVE_PLOT_UPDATE_FREQ} "
              f"for {config.NUM_CITIES} cities. This might be slow.")

    # Create plotter
    tsp_plotter = TSPPlotterSGA(cities)

    # Print parameters
    print(f"\nSGA Parameters: {sga_params}")

    # Create and run SGA
    sga = StandardGA(cities, distance_matrix)

    # Time the execution
    start_time = time.time()
    best_individual, cost_history = sga.solve(
        **sga_params,
        plotter=tsp_plotter
    )
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"SGA execution time: {execution_time:.2f} seconds")

    # Print final results
    print("\n" + "=" * 20 + " Final Results " + "=" * 20)
    print(f"Problem: {config.NUM_CITIES} cities (Seed: {config.CITY_SEED})")
    print(f"\nStandard GA (SGA):")
    print(f"  Best Cost: {best_individual.cost:.2f}")
    print(f"  Execution Time: {execution_time:.2f}s")

    # Update final plots
    tsp_plotter.display_execution_time(execution_time, cost_history)
    tsp_plotter.show_final_route(best_individual)
    tsp_plotter.convergence_ax.set_title("SGA Final Fitness Convergence")
    tsp_plotter.convergence_ax.legend(loc='upper right')

    print("\nCheck the plots for visual representation.")
    print("Close the plot window to end the script.")
    tsp_plotter.keep_plot_open()


if __name__ == "__main__":
    main()
