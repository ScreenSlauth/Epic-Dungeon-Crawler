import heapq
import math

def heuristic(a, b):
    """Manhattan distance heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """
    A* pathfinding algorithm to find the shortest path from start to goal
    
    Args:
        grid: 2D array where True means walkable, False means wall
        start: Tuple (x, y) of starting position
        goal: Tuple (x, y) of goal position
        
    Returns:
        List of (x, y) tuples representing the path from start to goal,
        or empty list if no path found
    """
    # Check if start or goal are invalid
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0
    
    if (not (0 <= start[0] < grid_width and 0 <= start[1] < grid_height) or
        not (0 <= goal[0] < grid_width and 0 <= goal[1] < grid_height)):
        return []
        
    if start == goal:
        return [start]
        
    # If goal is not walkable, cannot reach it
    if not grid[goal[1]][goal[0]]:
        return []
        
    # Initialize open and closed sets
    open_set = []
    closed_set = set()
    
    # Store g_score (cost from start) and f_score (g_score + heuristic)
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    # Store parent nodes to reconstruct path
    came_from = {}
    
    # Add start node to open set with priority f_score
    heapq.heappush(open_set, (f_score[start], start))
    
    # Define possible movement directions (up, right, down, left)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    while open_set:
        # Get node with lowest f_score
        _, current = heapq.heappop(open_set)
        
        # Check if goal reached
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
            
        # Mark node as processed
        closed_set.add(current)
        
        # Check all neighbors
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Skip if out of bounds
            if not (0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height):
                continue
                
            # Skip if not walkable or already processed
            if not grid[neighbor[1]][neighbor[0]] or neighbor in closed_set:
                continue
                
            # Calculate tentative g_score
            tentative_g_score = g_score[current] + 1
            
            # If neighbor not in open set or new path is better
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # Update path and scores
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                
                # Add to open set if not already there
                if neighbor not in [n for _, n in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
    # No path found
    return [] 