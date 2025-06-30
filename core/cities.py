"""City management for TSP."""


def get_fixed_cities():
    """Return a fixed set of cities for testing.

    Returns:
        list: List of (x, y) coordinate tuples for 10 cities
    """
    return [
        (60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
        (100, 160), (200, 160), (140, 140), (40, 120), (100, 120)
    ]
