import time
from collections import deque
from maze import Maze, MAZES

def solve_bfs(maze):
    """
    Executes a Breadth-First Search (BFS) to find the shortest path from Start to End.
    Returns a tuple: (winning_path_list, all_explored_nodes_list)
    """
    print("🌊 Launching Breadth-First Search (BFS) AI Agent...")
    start_time = time.time()
    
    # 1. THE QUEUE: Stores tuples of (current_position, path_taken_to_get_here)
    # We use a double-ended queue (deque) for instant O(1) pops from the left!
    queue = deque([(maze.start, [maze.start])])
    
    # 2. THE VISITED SET: Keeps track of coordinates we've already queued
    # Crucial to prevent infinite loops and cyclic backtracking!
    visited = {maze.start}
    
    # Track the order of exploration so we can visualize the AI's "thought process"
    explored_order = []
    
    while queue:
        # Pop the oldest coordinate from the FRONT of the line (First-In, First-Out)
        current_pos, path = queue.popleft()
        explored_order.append(current_pos)
        
        # Check if our AI has stepped onto the Finish Line!
        if current_pos == maze.end:
            elapsed_time = time.time() - start_time
            print(f"🏆 BFS SOLVED THE MAZE in {elapsed_time:.5f} seconds!")
            print(f"📊 Total Tiles Explored: {len(explored_order)}")
            print(f"⭐ Shortest Path Length:  {len(path)} steps")
            return path, explored_order
            
        # Discover all valid adjacent squares (Up, Down, Left, Right)
        for neighbor in maze.get_neighbors(current_pos):
            if neighbor not in visited:
                visited.add(neighbor)
                # Create a new path array by appending the new step to the existing path
                queue.append((neighbor, path + [neighbor]))
                
    # If the queue empties completely without finding the end, the maze is impossible!
    print("❌ BFS FAILED: No valid path exists from Start to End!")
    return None, explored_order

# --- TESTING THE BFS AI AGENT ---
if __name__ == "__main__":
    print("--- 🧪 TESTING BFS PATHFINDING ENGINE ---")
    
    # Load "The Cyber Labyrinth" from our built-in layouts
    test_data = MAZES["2"]
    maze = Maze(test_data["layout"])
    
    print(f"\n🗺️ Maze Loaded: {test_data['name']} ({maze.rows}x{maze.cols})")
    print("Showing empty grid:")
    maze.render()
    
    # Unleash the BFS AI
    winning_path, explored_tiles = solve_bfs(maze)
    
    if winning_path:
        print("\n🎨 Overlaying AI exploration (░░) and winning path (⭐)...")
        # Notice how we pass both the winning path and explored tiles into render!
        maze.render(path=winning_path, visited=explored_tiles)