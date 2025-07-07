#!/usr/bin/env python3
"""Main entry point for TSP solvers.

Author: Guglielmo Cimolai
Date: 07/07/2025
Version: v5
"""

import time
from core.cities import generate_cities
from core.distance import calculate_distance_matrix
from algorithms.sga import StandardGA
from algorithms.hga_aco import HybridGA_ACO
from visualization.plotter import TSPPlotter
import config


def get_adaptive_parameters(num_cities):
    """Get parameters adapted to problem size.

    Args:
        num_cities: Number of cities in the problem

    Returns:
        tuple: (sga_params, hga_params, plot_update_freq)
    """
    # SGA parameters
    sga_params = {
        "population_size": config.DEFAULT_SGA_POP_SIZE,
        "generations": config.DEFAULT_SGA_GENERATIONS,
        "crossover_rate": config.DEFAULT_SGA_CROSSOVER_RATE,
        "mutation_rate": config.DEFAULT_SGA_MUTATION_RATE,
        "elitism_size": config.DEFAULT_SGA_ELITISM_SIZE,
        "tournament_size": config.DEFAULT_SGA_TOURNAMENT_K
    }

    # HGA-ACO parameters
    hga_params = {
        "population_size": config.DEFAULT_HGA_POP_SIZE,
        "generations": config.DEFAULT_HGA_GENERATIONS,
        "ga_crossover_rate": config.DEFAULT_HGA_GA_CROSSOVER_RATE,
        "aco_contribution_rate": config.DEFAULT_HGA_ACO_CONTRIBUTION_RATE,
        "mutation_rate": config.DEFAULT_HGA_MUTATION_RATE,
        "elitism_size": config.DEFAULT_HGA_ELITISM_SIZE,
        "tournament_size": config.DEFAULT_HGA_TOURNAMENT_K,
        "alpha": config.DEFAULT_HGA_ALPHA,
        "beta": config.DEFAULT_HGA_BETA,
        "evaporation_rate": config.DEFAULT_HGA_EVAPORATION_RATE,
        "Q_pheromone": config.DEFAULT_HGA_Q_PHEROMONE,
        "initial_pheromone_val": config.DEFAULT_HGA_INITIAL_PHEROMONE,
        "best_n_deposit": config.DEFAULT_HGA_BEST_N_DEPOSIT
    }

    # Default plot frequency
    plot_freq = config.LIVE_PLOT_UPDATE_FREQ

    # Adapt parameters based on problem size
    if num_cities <= 50:
        sga_params.update({"generations": 750, "population_size": 100})
        hga_params.update({"generations": 250, "population_size": 100})
        plot_freq = 1
    elif num_cities <= 100:
        sga_params.update({"generations": 1500, "population_size": 200,
                           "elitism_size": 10})
        hga_params.update({"generations": 500, "population_size": 100})
        plot_freq = 5
    else:
        sga_params.update({"generations": 5000, "population_size": 200,
                           "elitism_size": 15})
        hga_params.update({"generations": 1000, "population_size": 200,
                           "elitism_size": 10, "best_n_deposit": 10})
        plot_freq = 10

    return sga_params, hga_params, plot_freq


def main():
    """Run TSP solver with both algorithms."""
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
    sga_params, hga_params, current_live_plot_freq = get_adaptive_parameters(config.NUM_CITIES)

    # Update global plot frequency
    config.LIVE_PLOT_UPDATE_FREQ = current_live_plot_freq

    # Performance warning
    if (config.NUM_CITIES > 100 and
            config.LIVE_PLOT_UPDATE_FREQ > 0 and
            config.LIVE_PLOT_UPDATE_FREQ < 10):
        print(f"INFO: Live plot update frequency is {config.LIVE_PLOT_UPDATE_FREQ} "
              f"for {config.NUM_CITIES} cities. This might be slow.")

    # Create plotter
    tsp_plotter = TSPPlotter(cities)

    # Run Standard GA
    print(f"\nSGA Parameters: {sga_params}")
    sga = StandardGA(cities, distance_matrix)

    start_time_sga = time.time()
    sga_best_individual, sga_cost_history = sga.solve(
        **sga_params,
        plotter=tsp_plotter
    )
    end_time_sga = time.time()
    sga_exec_time = end_time_sga - start_time_sga
    print(f"SGA execution time: {sga_exec_time:.2f} seconds")

    # Run Hybrid GA-ACO
    print(f"\nHGA-ACO Parameters: {hga_params}")
    hga = HybridGA_ACO(cities, distance_matrix)

    start_time_hga = time.time()
    hga_best_individual, hga_cost_history = hga.solve(
        **hga_params,
        plotter=tsp_plotter
    )
    end_time_hga = time.time()
    hga_exec_time = end_time_hga - start_time_hga
    print(f"HGA-ACO execution time: {hga_exec_time:.2f} seconds")

    # Final comparison
    print("\n" + "=" * 20 + " Final Comparison " + "=" * 20)
    print(f"Problem: {config.NUM_CITIES} cities (Seed: {config.CITY_SEED})")

    print(f"\nStandard GA (SGA):")
    print(f"  Best Cost: {sga_best_individual.cost:.2f}")
    print(f"  Execution Time: {sga_exec_time:.2f}s")

    print(f"\nHybrid GA-ACO (HGA-ACO):")
    print(f"  Best Cost: {hga_best_individual.cost:.2f}")
    print(f"  Execution Time: {hga_exec_time:.2f}s")

    # Calculate improvement
    improvement_abs = sga_best_individual.cost - hga_best_individual.cost
    improvement_rel = (improvement_abs / sga_best_individual.cost * 100) if sga_best_individual.cost > 0 else 0

    if hga_best_individual.cost < sga_best_individual.cost:
        print(f"\nHGA-ACO found a better solution by {improvement_abs:.2f} "
              f"({improvement_rel:.2f}% improvement).")
    elif sga_best_individual.cost < hga_best_individual.cost:
        print(f"\nSGA found a better solution by {-improvement_abs:.2f}.")
    else:
        print("\nBoth algorithms found solutions with the same cost.")

    # Update final plots
    tsp_plotter.display_execution_times(sga_exec_time, hga_exec_time)
    tsp_plotter.show_final_routes(sga_best_individual, hga_best_individual)
    tsp_plotter.convergence_ax.set_title("Final Fitness Convergence Comparison")
    tsp_plotter.convergence_ax.legend(loc='upper right')

    print("\nCheck the plots for visual comparison of routes and convergence.")
    print("Close the plot window to end the script.")
    tsp_plotter.keep_plot_open()


if __name__ == "__main__":
    main()
