"""Standard Genetic Algorithm implementation."""
import random
import copy
from algorithms.base import TSPAlgorithm
from core.individual import Individual


class StandardGA(TSPAlgorithm):
    """Standard Genetic Algorithm for TSP."""

    def __init__(self, cities, distance_matrix):
        """Initialize SGA.

        Args:
            cities: NumPy array of city coordinates
            distance_matrix: Pre-calculated distance matrix
        """
        super().__init__(cities, distance_matrix)

    def initialize_population(self, population_size):
        """Create initial random population.

        Args:
            population_size: Number of individuals in population

        Returns:
            list: List of Individual objects
        """
        population = []
        base_tour = list(range(self.num_cities))

        for _ in range(population_size):
            tour = random.sample(base_tour, self.num_cities)
            population.append(Individual(tour))

        return population

    def selection_tournament(self, population, tournament_size):
        """Tournament selection operator.

        Args:
            population: Current population
            tournament_size: Number of individuals in each tournament

        Returns:
            list: Selected parents (mating pool)
        """
        selected_parents = []

        # Create a mating pool of the same size as population
        for _ in range(len(population)):
            aspirants = random.sample(population, tournament_size)
            winner = min(aspirants, key=lambda ind: ind.cost)
            selected_parents.append(winner)

        return selected_parents

    def crossover_ordered(self, parent1_ind, parent2_ind):
        """Ordered crossover (OX) operator.

        Args:
            parent1_ind: First parent Individual
            parent2_ind: Second parent Individual

        Returns:
            Individual: Offspring individual
        """
        parent1_tour = parent1_ind.tour
        parent2_tour = parent2_ind.tour
        size = len(parent1_tour)

        # Initialize child tour with placeholders
        child_tour = [-1] * size

        # Select random segment from parent1
        start, end = sorted(random.sample(range(size), 2))
        child_tour[start:end + 1] = parent1_tour[start:end + 1]

        # Fill remaining positions from parent2
        p2_idx = 0
        for i in range(size):
            if child_tour[i] == -1:
                # Find next city from parent2 not already in child
                while parent2_tour[p2_idx] in child_tour[start:end + 1]:
                    p2_idx += 1
                child_tour[i] = parent2_tour[p2_idx]
                p2_idx += 1

        return Individual(child_tour)

    def mutate_swap(self, individual, mutation_prob):
        """Swap mutation operator.

        Args:
            individual: Individual to mutate
            mutation_prob: Probability of mutation
        """
        if random.random() < mutation_prob:
            tour = individual.tour
            idx1, idx2 = random.sample(range(len(tour)), 2)
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]

    def solve(self, population_size, generations, crossover_rate,
              mutation_rate, tournament_size, elitism_size=0):
        """Run the SGA to solve TSP.

        Args:
            population_size: Size of population
            generations: Number of generations to run
            crossover_rate: Probability of crossover
            mutation_rate: Probability of mutation
            tournament_size: Size of tournament for selection
            elitism_size: Number of best individuals to preserve

        Returns:
            Individual: Best solution found
        """
        # Initialize population
        population = self.initialize_population(population_size)

        # Evaluate initial population
        for ind in population:
            ind.calculate_cost(self.distance_matrix)

        # Sort and track best
        population.sort()
        self.best_individual = copy.deepcopy(population[0])

        print(f"\n--- Running SGA for {self.num_cities} cities ---")
        print(f"Initial best cost: {self.best_individual.cost:.2f}")

        # Evolution loop
        for gen in range(1, generations + 1):
            new_population = []

            # Apply elitism - preserve best individuals
            if elitism_size > 0:
                elites = copy.deepcopy(population[:elitism_size])
                new_population.extend(elites)

            # Create mating pool
            mating_pool = self.selection_tournament(population, tournament_size)

            # Generate offspring to fill population
            offspring_idx = 0
            while len(new_population) < population_size:
                # Select parents
                parent1 = mating_pool[offspring_idx % len(mating_pool)]
                offspring_idx += 1
                parent2 = mating_pool[offspring_idx % len(mating_pool)]
                offspring_idx += 1

                # Apply crossover
                if random.random() < crossover_rate:
                    child = self.crossover_ordered(parent1, parent2)
                else:
                    # Clone one parent if no crossover
                    child = copy.deepcopy(random.choice([parent1, parent2]))

                # Apply mutation
                self.mutate_swap(child, mutation_rate)

                # Evaluate offspring
                child.calculate_cost(self.distance_matrix)
                new_population.append(child)

            # Replace population
            population = new_population
            population.sort()

            # Update best if improved
            if population[0].cost < self.best_individual.cost:
                self.best_individual = copy.deepcopy(population[0])

            # Progress output
            if gen % 10 == 0 or gen == generations:
                print(f"SGA Gen {gen}/{generations} - Best Cost: {self.best_individual.cost:.2f}")

        print(f"SGA Final Best Tour: {self.best_individual.tour} with Cost: {self.best_individual.cost:.2f}")
        return self.best_individual
