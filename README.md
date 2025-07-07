# TSP Genetic Algorithm - Version 6

Multi-algorithm comparison framework for solving the Traveling Salesman Problem (TSP) featuring Standard Genetic Algorithm (SGA), Hybrid GA-ACO (HGA-ACO), and Particle Swarm Optimization (PSO).

## New Features in V6
- **Particle Swarm Optimization (PSO)**: Swarm intelligence algorithm for TSP
- **Algorithm toggle system**: Select any combination of algorithms to compare
- **Dynamic visualization**: Plotter adapts to show only selected algorithms
- **Flexible comparisons**: Compare 2 or 3 algorithms simultaneously
- **Velocity-based search**: PSO uses velocity vectors for discrete TSP

## Available Algorithm Combinations
1. **SGA vs HGA-ACO** (classic comparison)
2. **SGA vs PSO** (GA vs swarm intelligence)
3. **HGA-ACO vs PSO** (hybrid vs pure swarm)
4. **All three** (comprehensive comparison)

## Visualization
<img width="1000" alt="Plot" src="https://github.com/user-attachments/assets/dcd7631c-3015-48a8-bca5-d656e8806607" />

## Algorithms

### Standard GA (SGA)
- Tournament selection
- Ordered crossover
- Swap mutation
- Elitism

### Hybrid GA-ACO (HGA-ACO)
- Combines GA with Ant Colony Optimization
- Pheromone-guided construction
- Mixed population approach

### Particle Swarm Optimization (PSO)
- Swarm of particles exploring solution space
- Personal best (pBest) and global best (gBest) tracking
- Velocity-based position updates adapted for discrete TSP
- Social and cognitive learning components

Usage: `python main.py`
