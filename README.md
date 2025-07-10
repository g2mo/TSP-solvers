# TSP Solver Framework

A comprehensive multi-algorithm comparison framework for solving both static and dynamic Traveling Salesman Problems (TSP). Features Standard Genetic Algorithm (SGA), Hybrid GA-ACO (HGA-ACO), and Particle Swarm Optimization (PSO) with real-time visualization and performance analysis.

## 🚀 Key Features

### Dynamic TSP Support (New!)
- **Moving Cities**: Cities can move during algorithm execution, creating a dynamic optimization challenge
- **Real-time Adaptation**: Algorithms continuously adapt their solutions as cities move
- **Collision Avoidance**: Cities maintain minimum distance (1% of grid size) from each other
- **Reproducible Movement**: Seeded random movement patterns ensure fair algorithm comparison
- **Smooth Visualization**: Plot updates every generation when dynamic mode is active

### Multi-Algorithm Framework
- **Flexible Comparison**: Run any combination of SGA, HGA-ACO, and PSO
- **Adaptive Visualization**: Dynamic subplot layout adjusts to number of active algorithms
- **Performance Metrics**: Real-time convergence tracking and final performance comparison
- **Parameter Presets**: Automatic parameter optimization based on problem size

## 📊 Algorithms

### Standard Genetic Algorithm (SGA)
Classic evolutionary approach with:
- Tournament selection for parent selection
- Ordered crossover (OX) preserving relative city order
- Swap mutation for diversity
- Elitism to preserve best solutions

### Hybrid GA-ACO (HGA-ACO)
Innovative combination of genetic algorithms and ant colony optimization:
- Dual population: GA-evolved and ACO-constructed individuals
- Pheromone matrix guides solution construction
- Dynamic pheromone updates based on solution quality
- Balances exploration (ACO) and exploitation (GA)

### Particle Swarm Optimization (PSO)
Swarm intelligence adapted for discrete TSP:
- Velocity represented as swap sequences
- Personal best (pBest) and global best (gBest) tracking
- Optional 2-opt local search enhancement
- Cognitive and social learning components

## 🛠️ Installation

### Requirements
```bash
pip install -r requirements.txt
```

Dependencies:
- `numpy>=1.20.0`
- `matplotlib>=3.3.0`

### Project Structure
```
tsp-solver/
├── main.py                # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── algorithms/            # Algorithm implementations
│   ├── base.py            # Abstract base class
│   ├── sga.py             # Standard GA
│   ├── hga_aco.py         # Hybrid GA-ACO
│   └── pso.py             # Particle Swarm Optimization
├── core/                  # Core components
│   ├── cities.py          # City generation
│   ├── distance.py        # Distance calculations
│   ├── individual.py      # Solution representation
│   └── dynamic_cities.py  # Dynamic city management
└── visualization/         # Plotting utilities
    └── plotter.py         # Real-time visualization
```

## ⚙️ Configuration

Edit `config.py` to customize:

### Algorithm Selection
```python
ENABLE_SGA = True      # Standard Genetic Algorithm
ENABLE_HGA_ACO = True  # Hybrid GA-ACO
ENABLE_PSO = True      # Particle Swarm Optimization
```

### Problem Settings
```python
NUM_CITIES = 50       # Number of cities
CITY_SEED = 1         # Seed for reproducible city generation
CITY_WIDTH = 100      # Grid width
CITY_HEIGHT = 100     # Grid height
```

### Dynamic TSP Settings
```python
ENABLE_DYNAMIC_TSP = True      # Enable moving cities
DYNAMIC_MOVEMENT_SEED = 42     # Seed for reproducible movements
```

### Parameter Presets
The framework automatically selects optimal parameters based on problem size:
- **Small** (< 50 cities): Fast execution, testing
- **Medium** (50-100 cities): Balanced performance
- **Large** (> 100 cities): Maximum solution quality

## 🎮 Usage

### Basic Usage
```bash
python main.py
```

### Example Configurations

**Static TSP with All Algorithms:**
```python
# config.py
ENABLE_SGA = True
ENABLE_HGA_ACO = True
ENABLE_PSO = True
ENABLE_DYNAMIC_TSP = False
NUM_CITIES = 50
```

**Dynamic TSP with Selected Algorithms:**
```python
# config.py
ENABLE_SGA = True
ENABLE_HGA_ACO = True
ENABLE_PSO = False
ENABLE_DYNAMIC_TSP = True
NUM_CITIES = 30
```

**Large Problem with Custom Parameters:**
```python
# config.py
NUM_CITIES = 150
CUSTOM_PARAMS = {
    "SGA_POP_SIZE": 300,
    "SGA_GENERATIONS": 1000,
    # ... other parameters
}
```

## 📈 Visualization

The framework provides real-time visualization with:

### Route Evolution
- Live updates showing best tour for each algorithm
- City positions and labels
- Path optimization progress

### Convergence Tracking
- Cost evolution over generations
- Comparison across algorithms
- Execution time display

### Special Visualizations
- **Pheromone Heatmap** (HGA-ACO): Shows pheromone concentration
- **Performance Comparison**: Bar charts comparing solution quality and efficiency

### Dynamic TSP Visualization
When `ENABLE_DYNAMIC_TSP = True`:
- Cities move smoothly across the grid
- Fitness curves show realistic fluctuations
- Plot updates every generation for smooth animation
- Final routes optimized for actual city positions

<img width="800" height="600" alt="Plot" src="https://github.com/user-attachments/assets/3cdd7161-df15-4ed9-a62d-2274e309b0e3" />

## 🔧 Technical Details

### Dynamic City Movement
- **Movement Duration**: 150-300 generations per segment
- **Direction**: Random target selection
- **Speed**: Linear interpolation between start and end points
- **Collision Detection**: Automatic path recalculation on collision
- **Reproducibility**: Seeded random generator ensures identical movements across algorithm runs

### Cost Tracking
- **Static Mode**: Traditional best-cost tracking
- **Dynamic Mode**: Actual current cost tracking (may increase when cities move)
- **Re-evaluation**: All solutions re-evaluated when city positions change

### Performance Optimization
- Pre-calculated distance matrices
- Efficient numpy operations
- Optimized visualization updates
- Configurable plot frequencies

## 📊 Output Analysis

The framework provides comprehensive analysis including:

1. **Final Comparison**
   - Best solution cost for each algorithm
   - Execution time comparison
   - Pairwise performance differences

2. **Visual Analysis**
   - Final optimized routes
   - Convergence behavior
   - Performance metrics

3. **Dynamic TSP Insights**
   - Adaptation speed to changes
   - Solution stability
   - Recovery from disruptions

## 🎯 Use Cases

1. **Algorithm Research**: Compare metaheuristic performance
2. **Dynamic Optimization**: Study adaptation to changing environments
3. **Parameter Tuning**: Find optimal settings for specific problems
4. **Educational**: Visualize evolutionary and swarm algorithms
5. **Benchmarking**: Test new algorithms against established methods

## 🤝 Contributing

Contributions are welcome! To add a new algorithm:

1. Create new file in `algorithms/`
2. Inherit from `TSPAlgorithm` base class
3. Implement `solve()` method
4. Add algorithm toggle in `config.py`
5. Update visualization colors in `plotter.py`

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
