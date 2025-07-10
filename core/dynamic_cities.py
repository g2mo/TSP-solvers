"""Dynamic city management for Dynamic TSP."""
import numpy as np
import random


class DynamicCityManager:
    """Manages moving cities for Dynamic TSP."""

    def __init__(self, initial_cities, grid_width, grid_height, movement_seed=42):
        """Initialize dynamic city manager.

        Args:
            initial_cities: NumPy array of initial (x, y) coordinates
            grid_width: Width of the grid
            grid_height: Height of the grid
            movement_seed: Seed for reproducible random movements
        """
        self.num_cities = len(initial_cities)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.movement_seed = movement_seed

        # Calculate minimum distance (1% of grid size)
        self.min_distance = 0.01 * np.sqrt(grid_width ** 2 + grid_height ** 2)

        # Store initial positions for reset
        self.initial_positions = initial_cities.copy()

        # Current positions (will be updated)
        self.positions = initial_cities.copy().astype(float)

        # Movement parameters for each city
        self.targets = np.zeros_like(self.positions)
        self.movement_start_positions = np.zeros_like(self.positions)
        self.movement_generations = np.zeros(self.num_cities, dtype=int)
        self.current_movement_step = np.zeros(self.num_cities, dtype=int)

        # Random generator for reproducible movements
        self.rng = random.Random(movement_seed)
        self.np_rng = np.random.RandomState(movement_seed)

        # Initialize first movements
        self.reset_movements()

    def reset_to_initial(self):
        """Reset cities to initial positions and reinitialize movements."""
        self.positions = self.initial_positions.copy().astype(float)

        # Reset random generators with same seed
        self.rng = random.Random(self.movement_seed)
        self.np_rng = np.random.RandomState(self.movement_seed)

        # Reset movement parameters
        self.targets = np.zeros_like(self.positions)
        self.movement_start_positions = np.zeros_like(self.positions)
        self.movement_generations = np.zeros(self.num_cities, dtype=int)
        self.current_movement_step = np.zeros(self.num_cities, dtype=int)

        # Initialize movements again
        self.reset_movements()

    def reset_movements(self):
        """Initialize movement parameters for all cities."""
        for i in range(self.num_cities):
            self._set_new_target(i)

    def _set_new_target(self, city_idx):
        """Set a new random target for a city.

        Args:
            city_idx: Index of the city
        """
        # Random movement duration between 150-300 generations
        self.movement_generations[city_idx] = self.rng.randint(500, 1000)
        self.current_movement_step[city_idx] = 0

        # Store starting position
        self.movement_start_positions[city_idx] = self.positions[city_idx].copy()

        # Random target position anywhere on grid
        self.targets[city_idx] = np.array([
            self.rng.uniform(0, self.grid_width),
            self.rng.uniform(0, self.grid_height)
        ])

    def _check_collision(self, city_idx, new_position):
        """Check if new position would cause collision.

        Args:
            city_idx: Index of the moving city
            new_position: Proposed new position

        Returns:
            bool: True if collision would occur
        """
        for i in range(self.num_cities):
            if i != city_idx:
                distance = np.linalg.norm(new_position - self.positions[i])
                if distance < self.min_distance:
                    return True
        return False

    def update_positions(self):
        """Update all city positions for one generation."""
        for i in range(self.num_cities):
            if self.current_movement_step[i] >= self.movement_generations[i]:
                # Movement complete, set new target
                self._set_new_target(i)

            # Calculate next position
            progress = (self.current_movement_step[i] + 1) / self.movement_generations[i]
            direction = self.targets[i] - self.movement_start_positions[i]
            new_position = self.movement_start_positions[i] + progress * direction

            # Check for collision
            if self._check_collision(i, new_position):
                # Collision detected, pick new target
                self._set_new_target(i)
                # Don't move this generation
                continue

            # Update position
            self.positions[i] = new_position
            self.current_movement_step[i] += 1

    def get_current_positions(self):
        """Get current city positions.

        Returns:
            np.ndarray: Current (x, y) coordinates of all cities
        """
        return self.positions.copy()
