"""Individual representation for GA."""
from core.distance import calculate_tour_cost


class Individual:
    """Represents a solution (tour) in the GA population."""

    def __init__(self, tour):
        """Initialize an individual with a tour.

        Args:
            tour: List of city indices representing the tour
        """
        self.tour = list(tour)
        self.cost = float('inf')

    def calculate_cost(self, distance_matrix):
        """Calculate and store the tour cost.

        Args:
            distance_matrix: NumPy 2D array of distances between cities

        Returns:
            float: The calculated cost
        """
        self.cost = calculate_tour_cost(self.tour, distance_matrix)
        return self.cost

    def __lt__(self, other):
        """Enable sorting by cost."""
        return self.cost < other.cost

    def __repr__(self):
        """String representation for console output."""
        # Shorten tour representation if too long
        if len(self.tour) < 15:
            tour_str = str(self.tour)
        else:
            tour_str = str(self.tour[:7] + ["..."] + self.tour[-7:])
        return f"Tour: {tour_str} Cost: {self.cost:.2f}"
