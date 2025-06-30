"""Distance calculations for TSP."""
import math


def euclidean_distance(city1, city2):
    """Compute Euclidean distance between two cities.

    Args:
        city1: Tuple of (x, y) coordinates
        city2: Tuple of (x, y) coordinates

    Returns:
        float: Euclidean distance
    """
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calculate_distance_matrix(cities):
    """Calculate distance matrix for all city pairs.

    Args:
        cities: List of (x, y) coordinate tuples

    Returns:
        list: 2D list of distances between cities
    """
    num_cities = len(cities)
    # Initialize distance matrix with zeros using nested lists
    dist_matrix = [[0.0 for _ in range(num_cities)] for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            dist = euclidean_distance(cities[i], cities[j])
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist

    return dist_matrix


def calculate_tour_cost(tour, distance_matrix):
    """Calculate total cost (distance) for a complete tour.

    Args:
        tour: List of city indices representing the tour
        distance_matrix: 2D list of distances between cities

    Returns:
        float: Total tour distance
    """
    cost = 0.0
    num_cities = len(tour)
    for i in range(num_cities):
        cost += distance_matrix[tour[i]][tour[(i + 1) % num_cities]]
    return cost
