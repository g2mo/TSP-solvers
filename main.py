#!/usr/bin/env python3
"""Main entry point for TSP solver with multiple algorithms.

Author: Guglielmo Cimolai
Date: 10/07/2025
Version: v7
"""

import time
from core.cities import generate_cities
from core.distance import calculate_distance_matrix
from algorithms.sga import StandardGA
from algorithms.hga_aco import HybridGA_ACO
from algorithms.pso import ParticleSwarmOptimization
from visualization.plotter import TSPPlotter
import config
from core.dynamic_cities import DynamicCityManager


def get_enabled_algorithms():
    """Get dictionary of enabled algorithms from config.

    Returns:
        dict: Algorithm names mapped to enabled status
    """
    return {
        "SGA": config.ENABLE_SGA,
        "HGA-ACO": config.ENABLE_HGA_ACO,
        "PSO": config.ENABLE_PSO
    }


def print_parameter_summary(params_dict, num_cities):
    """Print a summary of the parameters being used.

    Args:
        params_dict: Dictionary of all parameters
        num_cities: Number of cities in the problem
    """
    print("\n" + "=" * 30)
    print(f"PARAMETER CONFIGURATION FOR {num_cities} CITIES")
    print("=" * 30)

    if num_cities < 50:
        print("Problem Size: SMALL (< 50 cities)")
    elif num_cities <= 100:
        print("Problem Size: MEDIUM (50-100 cities)")
    else:
        print("Problem Size: LARGE (> 100 cities)")

    print("\nKey Parameters:")
    print(f"  Visualization Update: Every {params_dict.get('LIVE_PLOT_UPDATE_FREQ', 10)} generations")

    if config.ENABLE_SGA:
        print("\nSGA Parameters:")
        print(f"  Population: {params_dict.get('SGA_POP_SIZE', 'N/A')}")
        print(f"  Generations: {params_dict.get('SGA_GENERATIONS', 'N/A')}")
        print(f"  Crossover Rate: {params_dict.get('SGA_CROSSOVER_RATE', 'N/A')}")
        print(f"  Mutation Rate: {params_dict.get('SGA_MUTATION_RATE', 'N/A')}")

    if config.ENABLE_HGA_ACO:
        print("\nHGA-ACO Parameters:")
        print(f"  Population: {params_dict.get('HGA_POP_SIZE', 'N/A')}")
        print(f"  Generations: {params_dict.get('HGA_GENERATIONS', 'N/A')}")
        print(f"  ACO Contribution: {params_dict.get('HGA_ACO_CONTRIBUTION_RATE', 'N/A')}")
        print(f"  Alpha/Beta: {params_dict.get('HGA_ALPHA', 'N/A')}/{params_dict.get('HGA_BETA', 'N/A')}")

    if config.ENABLE_PSO:
        print("\nPSO Parameters:")
        print(f"  Particles: {params_dict.get('PSO_NUM_PARTICLES', 'N/A')}")
        print(f"  Generations: {params_dict.get('PSO_GENERATIONS', 'N/A')}")
        print(f"  Inertia (w): {params_dict.get('PSO_W', 'N/A')}")
        print(f"  Local Search: {'Enabled' if params_dict.get('PSO_USE_LOCAL_SEARCH', True) else 'Disabled'}")

    print("=" * 50 + "\n")


def get_algorithm_parameters(num_cities):
    """Get algorithm parameters based on problem size.

    Args:
        num_cities: Number of cities in the problem

    Returns:
        tuple: (sga_params, hga_params, pso_params, plot_freq)
    """
    # Get appropriate parameter set
    if config.CUSTOM_PARAMS:
        params = config.CUSTOM_PARAMS
        print(f"Using custom parameters")
    else:
        params = config.get_problem_params(num_cities)
        if num_cities < 50:
            print(f"Using parameters for small problems (< 50 cities)")
        elif num_cities <= 100:
            print(f"Using parameters for medium problems (50-100 cities)")
        else:
            print(f"Using parameters for large problems (> 100 cities)")

    # Extract SGA parameters
    sga_params = {
        "population_size": params.get("SGA_POP_SIZE", 100),
        "generations": params.get("SGA_GENERATIONS", 200),
        "crossover_rate": params.get("SGA_CROSSOVER_RATE", 0.85),
        "mutation_rate": params.get("SGA_MUTATION_RATE", 0.15),
        "elitism_size": params.get("SGA_ELITISM_SIZE", 5),
        "tournament_size": params.get("SGA_TOURNAMENT_K", 3)
    }

    # Extract HGA-ACO parameters
    hga_params = {
        "population_size": params.get("HGA_POP_SIZE", 100),
        "generations": params.get("HGA_GENERATIONS", 200),
        "ga_crossover_rate": params.get("HGA_GA_CROSSOVER_RATE", 0.7),
        "aco_contribution_rate": params.get("HGA_ACO_CONTRIBUTION_RATE", 0.5),
        "mutation_rate": params.get("HGA_MUTATION_RATE", 0.15),
        "elitism_size": params.get("HGA_ELITISM_SIZE", 5),
        "tournament_size": params.get("HGA_TOURNAMENT_K", 3),
        "alpha": params.get("HGA_ALPHA", 1.0),
        "beta": params.get("HGA_BETA", 3.0),
        "evaporation_rate": params.get("HGA_EVAPORATION_RATE", 0.3),
        "Q_pheromone": params.get("HGA_Q_PHEROMONE", 100.0),
        "initial_pheromone_val": params.get("HGA_INITIAL_PHEROMONE", 0.1),
        "best_n_deposit": params.get("HGA_BEST_N_DEPOSIT", 5)
    }

    # Extract PSO parameters
    pso_params = {
        "num_particles": params.get("PSO_NUM_PARTICLES", 30),
        "generations": params.get("PSO_GENERATIONS", 200),
        "w": params.get("PSO_W", 0.5),
        "c1": params.get("PSO_C1", 2.0),
        "c2": params.get("PSO_C2", 2.0),
        "use_local_search": params.get("PSO_USE_LOCAL_SEARCH", True)
    }

    # Get plot frequency
    plot_freq = params.get("LIVE_PLOT_UPDATE_FREQ", 1)

    return sga_params, hga_params, pso_params, plot_freq


def main():
    """Run TSP solver with selected algorithms."""
    # Check which algorithms are enabled
    enabled_algorithms = get_enabled_algorithms()
    num_enabled = sum(enabled_algorithms.values())

    if num_enabled == 0:
        print("Error: No algorithms enabled! Enable at least one algorithm in config.py")
        return

    # Generate cities
    cities = generate_cities(
        config.NUM_CITIES,
        width=config.CITY_WIDTH,
        height=config.CITY_HEIGHT,
        seed=config.CITY_SEED
    )

    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(cities)

    # Initialize dynamic city manager if enabled
    dynamic_city_manager = None
    if config.ENABLE_DYNAMIC_TSP:
        print("\n*** DYNAMIC TSP MODE ENABLED ***")
        print("Cities will move during algorithm execution")
        dynamic_city_manager = DynamicCityManager(
            cities,
            config.CITY_WIDTH,
            config.CITY_HEIGHT,
            config.DYNAMIC_MOVEMENT_SEED
        )

    print("Multi-Algorithm TSP Solver")
    print(f"Comparing: {', '.join([algo for algo, enabled in enabled_algorithms.items() if enabled])}")
    print(f"\nGenerated {config.NUM_CITIES} cities. Distance matrix calculated.")

    # Get algorithm parameters
    sga_params, hga_params, pso_params, plot_freq = get_algorithm_parameters(config.NUM_CITIES)

    # Override plot frequency for dynamic TSP
    if config.ENABLE_DYNAMIC_TSP:
        plot_freq = 1  # Update every generation for smooth city movement visualization
        print("Plot update frequency set to 1 for dynamic TSP visualization")

    config.LIVE_PLOT_UPDATE_FREQ = plot_freq

    # Print parameter summary
    all_params = config.CUSTOM_PARAMS if config.CUSTOM_PARAMS else config.get_problem_params(config.NUM_CITIES)
    print_parameter_summary(all_params, config.NUM_CITIES)

    # Create plotter with enabled algorithms
    tsp_plotter = TSPPlotter(cities, enabled_algorithms)

    # Store results
    results = {}
    exec_times = {}

    # Run SGA if enabled
    if enabled_algorithms["SGA"]:
        # Reset dynamic cities for fair comparison
        if dynamic_city_manager:
            dynamic_city_manager.reset_to_initial()

        sga = StandardGA(cities, distance_matrix)

        start_time = time.time()
        sga_best, sga_history = sga.solve(**sga_params, plotter=tsp_plotter, dynamic_city_manager=dynamic_city_manager)
        end_time = time.time()

        exec_times["SGA"] = end_time - start_time
        results["SGA"] = sga_best
        print(f"SGA execution time: {exec_times['SGA']:.2f} seconds")

    # Run HGA-ACO if enabled
    if enabled_algorithms["HGA-ACO"]:
        # Reset dynamic cities for fair comparison
        if dynamic_city_manager:
            dynamic_city_manager.reset_to_initial()

        hga = HybridGA_ACO(cities, distance_matrix)

        start_time = time.time()
        hga_best, hga_history = hga.solve(**hga_params, plotter=tsp_plotter, dynamic_city_manager=dynamic_city_manager)
        end_time = time.time()

        exec_times["HGA-ACO"] = end_time - start_time
        results["HGA-ACO"] = hga_best
        print(f"HGA-ACO execution time: {exec_times['HGA-ACO']:.2f} seconds")

    # Run PSO if enabled
    if enabled_algorithms["PSO"]:
        # Reset dynamic cities for fair comparison
        if dynamic_city_manager:
            dynamic_city_manager.reset_to_initial()

        pso = ParticleSwarmOptimization(cities, distance_matrix)

        start_time = time.time()
        pso_best, pso_history = pso.solve(**pso_params, plotter=tsp_plotter, dynamic_city_manager=dynamic_city_manager)
        end_time = time.time()

        exec_times["PSO"] = end_time - start_time
        results["PSO"] = pso_best
        print(f"PSO execution time: {exec_times['PSO']:.2f} seconds")

    # Final comparison
    print("\n" + "=" * 30 + " Final Comparison " + "=" * 30)
    print(f"Problem: {config.NUM_CITIES} cities (Seed: {config.CITY_SEED})")

    # Display results for each algorithm
    for algo, best_ind in results.items():
        print(f"\n{algo}:")
        print(f"  Best Cost: {best_ind.cost:.2f}")
        print(f"  Execution Time: {exec_times[algo]:.2f}s")

    # Find overall best
    best_algo = min(results.keys(), key=lambda a: results[a].cost)
    print(f"\nBest solution found by: {best_algo}")

    # Compare algorithms pairwise
    if num_enabled > 1:
        print("\nPairwise comparisons:")
        algo_list = list(results.keys())
        for i in range(len(algo_list)):
            for j in range(i + 1, len(algo_list)):
                algo1, algo2 = algo_list[i], algo_list[j]
                diff = results[algo1].cost - results[algo2].cost
                if diff > 0:
                    print(f"  {algo2} beat {algo1} by {diff:.2f}")
                elif diff < 0:
                    print(f"  {algo1} beat {algo2} by {-diff:.2f}")
                else:
                    print(f"  {algo1} and {algo2} found equal solutions")

    # Get final city positions for display
    final_cities = dynamic_city_manager.get_current_positions() if dynamic_city_manager else None

    # Update final plots
    tsp_plotter.display_execution_times(exec_times)
    tsp_plotter.show_final_routes(results, current_cities=final_cities)
    tsp_plotter.show_performance_comparison(results, exec_times)
    tsp_plotter.convergence_ax.set_title("Final Fitness Convergence Comparison")

    if config.ENABLE_DYNAMIC_TSP:
        print(f"Dynamic TSP enabled (Movement Seed: {config.DYNAMIC_MOVEMENT_SEED})")

    print("\nCheck the plots for visual comparison.")
    print("Close the plot window to end the script.")
    tsp_plotter.keep_plot_open()


if __name__ == "__main__":
    main()
