"""Base class for TSP algorithms."""
from abc import ABC, abstractmethod


class TSPAlgorithm(ABC):
    """Abstract base class for TSP solving algorithms."""

    def __init__(self, cities, distance_matrix):
        """Initialize algorithm with problem data.

        Args:
            cities: NumPy array of city coordinates
            distance_matrix: Pre-calculated distance matrix
        """
        self.cities = cities
        self.distance_matrix = distance_matrix
        self.num_cities = len(cities)
        self.best_individual = None
        self.cost_history = []  # Track cost over generations
        self.dynamic_city_manager = None  # For dynamic TSP

    def update_distance_matrix(self, new_cities):
        """Update distance matrix with new city positions.

        Args:
            new_cities: Updated city coordinates
        """
        from core.distance import calculate_distance_matrix
        self.cities = new_cities
        self.distance_matrix = calculate_distance_matrix(new_cities)

    @abstractmethod
    def solve(self, **kwargs):
        """Solve the TSP problem.

        Returns:
            tuple: (best_individual, cost_history)
        """
        pass
