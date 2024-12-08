# Search Algorithms Visualization

This project visualizes various search algorithms using Pygame. It includes implementations for A* search, Bidirectional search, and Breadth-First Search (BFS). The visualization allows users to create a grid, set start and goal positions, and run the algorithms to see how they find paths.

![Search Algorithms Visualization](images/Capture.png)

## Prerequisites

- Python 
- Pygame library

## Files

- `main.py`: Main script that runs the visualization.
- `cell.py`: Contains the `Cell` class used to represent each cell in the grid.
- `settings.py`: Contains configuration settings such as colors and grid dimensions.

## Controls
- Left-click to draw obstacles.
- Right-click to remove obstacles.
- Press the space bar to run the selected search algorithm.

## Algorithm Selection
You can change the algorithm by modifying the STRATEGY variable in settings.py:
- STRATEGY = 1: A* Search
- STRATEGY = 2: Bidirectional Search
- STRATEGY = 3: Breadth-First Search (BFS)
