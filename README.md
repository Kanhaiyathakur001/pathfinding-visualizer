Pathfinding Visualizer using BFS, DFS, and A-Star
An interactive visualization tool to demonstrate and compare the performance of classic pathfinding algorithms on a 2D grid.

Description
This project is a graphical application that brings pathfinding algorithms to life. Users can interact with a grid, define obstacles, and watch as BFS, DFS, and A-Star algorithms find the shortest or a valid path from a start point to an end point. The tool is designed to be an educational aid, providing a clear visual representation of how each algorithm explores the search space.

Key Features
Algorithm Visualization: Watch the traversal process of BFS, DFS, and A-Star in real time.

Maze Generation: The visualization can be used to solve complex mazes by drawing walls.

Performance Comparison: See how different algorithms explore the grid and find paths.

A-Star Heuristics: The A* algorithm uses a heuristic function (Manhattan distance) to guide its search efficiently towards the target, demonstrating its power.

Interactive Grid: Use the mouse to set the start node, end node, and draw walls.

Technologies Used
Python: The core programming language.

Pygame: Used for the graphical user interface and real-time visualization.

Data Structures & Algorithms: Leverages queues for BFS, stacks for DFS, and priority queues with a heap for A* search.

Prerequisites
To run this project, you need to have Python and the pygame library installed. You can install pygame using pip:

pip install pygame

Installation
Clone the repository:

git clone https://github.com/Kanhaiyathakur001/pathfinding-visualizer.git
cd pathfinding-visualizer

Install dependencies:

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file manually with the line pygame in it.)

Usage
Run the script from your terminal:

python pathfinding_visualizer.py

Controls:

Left Mouse Button:

Click once to set the start node (orange).

Click a second time to set the end node (turquoise).

Click to draw walls (black).

Right Mouse Button: Erase a wall or reset the start/end node.

Keyboard:

Press 1 to run BFS.

Press 2 to run DFS.

Press 3 to run A-Star.

Press C to clear the entire grid.

