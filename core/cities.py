"""City management for TSP."""
import random
import numpy as np


def get_fixed_cities():
    """Return a fixed set of cities for testing.
    
    Returns:
        np.ndarray: Array of (x, y) coordinates for 10 cities
    """
    cities = [
        (60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
        (100, 160), (200, 160), (140, 140), (40, 120), (100, 120)
    ]
    return np.array(cities)


def generate_cities(num_cities, width=100, height=100, seed=None):
    """Generate random cities in a given space.
    
    Args:
        num_cities: Number of cities to generate
        width: Width of the grid (default: 100)
        height: Height of the grid (default: 100)
        seed: Random seed for reproducibility (default: None)
        
    Returns:
        np.ndarray: Array of (x, y) coordinates
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    cities = []
    for _ in range(num_cities):
        x = random.randint(0, width)
        y = random.randint(0, height)
        cities.append((x, y))
    
    return np.array(cities)
