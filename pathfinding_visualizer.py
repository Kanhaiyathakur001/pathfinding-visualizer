import pygame
from collections import deque
import heapq
import sys

# --- Pygame Initialization ---
pygame.init()

# Define screen dimensions
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")

# --- Colors ---
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# --- Node Class ---
class Node:
    """
    Represents a single point (node) on the grid.
    """
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        """
        Returns the (row, col) position of the node.
        """
        return self.row, self.col
    
    def is_closed(self):
        """
        Checks if the node has been visited.
        """
        return self.color == RED

    def is_open(self):
        """
        Checks if the node is in the open set (queue or priority queue).
        """
        return self.color == GREEN

    def is_wall(self):
        """
        Checks if the node is a wall (obstacle).
        """
        return self.color == BLACK
    
    def is_start(self):
        """
        Checks if the node is the starting point.
        """
        return self.color == ORANGE
    
    def is_end(self):
        """
        Checks if the node is the end point.
        """
        return self.color == TURQUOISE

    def reset(self):
        """
        Resets the node's color to white.
        """
        self.color = WHITE
        
    def make_start(self):
        """
        Sets the node as the start point.
        """
        self.color = ORANGE
    
    def make_closed(self):
        """
        Sets the node as closed (visited).
        """
        self.color = RED
    
    def make_open(self):
        """
        Sets the node as open (in the search queue).
        """
        self.color = GREEN
    
    def make_wall(self):
        """
        Sets the node as a wall.
        """
        self.color = BLACK
    
    def make_end(self):
        """
        Sets the node as the end point.
        """
        self.color = TURQUOISE
    
    def make_path(self):
        """
        Sets the node as part of the final path.
        """
        self.color = PURPLE

    def draw(self, win):
        """
        Draws the node on the Pygame window.
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """
        Finds valid neighbors for the node (not walls).
        """
        self.neighbors = []
        # Check Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Check Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

# --- Grid Functions ---
def make_grid(rows, width):
    """
    Creates a 2D list representing the grid of nodes.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    """
    Draws the grid lines on the window.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    """
    Draws all the nodes and the grid lines.
    """
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    """
    Converts a mouse click position into a (row, col) grid position.
    """
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# --- Path Reconstruction ---
def reconstruct_path(came_from, current, draw):
    """
    Backtracks from the end node to reconstruct and draw the shortest path.
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# --- Algorithms ---

def bfs(draw, grid, start, end):
    """
    Breadth-First Search algorithm.
    """
    queue = deque([start])
    visited = {start}
    came_from = {}
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = queue.popleft()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def dfs(draw, grid, start, end):
    """
    Depth-First Search algorithm.
    """
    stack = [start]
    visited = {start}
    came_from = {}
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = stack.pop()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def h(p1, p2):
    """
    Heuristic function for A* (Manhattan distance).
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(draw, grid, start, end):
    """
    A* Search algorithm.
    """
    count = 0
    open_set = [(0, count, start)] # f_score, counter, node
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

# --- Main Loop ---
def main(win, width):
    """
    The main game loop that handles user input and visualizes algorithms.
    """
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Left mouse button actions
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()
            
            # Right mouse button actions (reset node)
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            # Keyboard commands
            if event.type == pygame.KEYDOWN:
                # Start BFS algorithm on '1' key press
                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # Start DFS algorithm on '2' key press
                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Start A* algorithm on '3' key press
                if event.key == pygame.K_3 and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Reset the grid on 'c' key press
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
