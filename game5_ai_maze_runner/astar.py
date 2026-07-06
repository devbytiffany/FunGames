import time
import heapq
from maze import Maze, MAZES

def manhattan_distance(pos1, pos2):
    """
    Calculates the grid-based distance between two coordinates: |r1 - r2| + |c1 - c2|
    This acts as the AI's 'compass', estimating how far away the finish line is!
    """
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2)

def solve_astar(maze):
    """
    Executes an A* Pathfinding search using a Priority Queue (Min-Heap).
    Returns a tuple: (winning_path_list, all_explored_nodes_list)
    """
    print("🧠 Launching A* (A-Star) Intelligent Heuristic Agent...")
    start_time = time.time()
    
    # 1. THE PRIORITY QUEUE (Min-Heap):
    # We store tuples formatted as: (f_score, tie_breaker_id, current_pos, path, g_score)
    # heapq automatically sorts and pops the item with the smallest f_score first!
    open_set = []
    
    # Calculate initial scores for the Start position
    start_g = 0
    start_h = manhattan_distance(maze.start, maze.end)
    start_f = start_g + start_h
    
    # tie_breaker prevents crashes if two tiles have the exact same f_score
    tie_breaker = 0 
    heapq.heappush(open_set, (start_f, tie_breaker, maze.start, [maze.start], start_g))
    
    # 2. THE G-SCORE DICTIONARY: Tracks the cheapest known cost to reach any coordinate.
    # If we find a faster shortcut to a tile we've already seen, we update it!
    g_scores = {maze.start: start_g}
    
    # Track exploration order for visualization
    explored_order = []
    
    while open_set:
        # Pop the tile with the ABSOLUTE LOWEST f_score (Best estimated path so far)
        f_score, _, current_pos, path, g_score = heapq.heappop(open_set)
        
        # We record exploration when a node is actually popped and processed
        if current_pos not in explored_order:
            explored_order.append(current_pos)
        
        # Check if we reached the finish line!
        if current_pos == maze.end:
            elapsed_time = time.time() - start_time
            print(f"🏆 A* SOLVED THE MAZE in {elapsed_time:.5f} seconds!")
            print(f"📊 Total Tiles Explored: {len(explored_order)}")
            print(f"⭐ Shortest Path Length:  {len(path)} steps")
            return path, explored_order
            
        # Discover open adjacent squares
        for neighbor in maze.get_neighbors(current_pos):
            # Taking a step to an adjacent square costs exactly 1 more step
            tentative_g = g_score + 1
            
            # If this is a brand new tile OR we found a shorter path to a known tile:
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                
                # Calculate new Heuristic and Total scores
                h_score = manhattan_distance(neighbor, maze.end)
                f_score = tentative_g + h_score
                
                tie_breaker += 1
                heapq.heappush(open_set, (f_score, tie_breaker, neighbor, path + [neighbor], tentative_g))
                
    print("❌ A* FAILED: No valid path exists from Start to End!")
    return None, explored_order

# --- TESTING THE A* AI AGENT ---
if __name__ == "__main__":
    print("--- 🧪 TESTING A* PATHFINDING ENGINE ---")
    
    # Load the exact same "Cyber Labyrinth" we tested with BFS!
    test_data = MAZES["2"]
    maze = Maze(test_data["layout"])
    
    print(f"\n🗺️ Maze Loaded: {test_data['name']} ({maze.rows}x{maze.cols})")
    
    # Unleash the A* AI
    winning_path, explored_tiles = solve_astar(maze)
    
    if winning_path:
        print("\n🎨 Overlaying AI exploration (░░) and winning path (⭐)...")
        maze.render(path=winning_path, visited=explored_tiles)