import sys
import time
from maze import Maze, MAZES
from bfs import solve_bfs
from astar import solve_astar

def print_header():
    """Prints the AI Racing Console banner."""
    print("\n" + "="*60)
    print(" 🤖  ALGORITHMIC AI MAZE RUNNER & BENCHMARK SUITE  🤖 ")
    print("="*60)
    print(" COMPETE: Unweighted BFS vs. Heuristic A* vs. HUMAN")
    print(" GOAL: Find the shortest path with minimum memory (tiles explored).")
    print("="*60)

def select_maze():
    """Allows the user to select a built-in maze layout from maze.py."""
    print("\n--- 🗺️ SELECT MAZE DIFFICULTY ---")
    for key, data in MAZES.items():
        print(f"  [{key}] {data['name']}")
    
    choice = input("\nEnter maze number (default: 2): ").strip()
    if choice not in MAZES:
        print("💡 Defaulting to [2] The Cyber Labyrinth...")
        return MAZES["2"]
    return MAZES[choice]

def run_individual_test(algo_name, maze_data):
    """Runs and visualizes a single AI algorithm."""
    maze = Maze(maze_data["layout"])
    print(f"\n🚀 Launching {algo_name} on [{maze_data['name']}]...")
    print("Initial Grid:")
    maze.render()
    
    time.sleep(0.5) # Brief pause for visual pacing
    
    if algo_name == "BFS":
        path, explored = solve_bfs(maze)
    else:
        path, explored = solve_astar(maze)
        
    if path:
        print(f"\n🎨 {algo_name} Exploration Map:")
        maze.render(path=path, visited=explored)
    input("\nPress Enter to return to the main menu...")

def run_benchmark_race(maze_data):
    """
    Pits BFS and A* against each other on the exact same layout
    and prints a clean performance comparison table!
    """
    print(f"\n" + "🏁"*30)
    print(f" THE ALGORITHM SHOWDOWN: [{maze_data['name']}] ")
    print("🏁"*30)
    
    # --- RUN BFS ---
    maze_bfs = Maze(maze_data["layout"])
    t0 = time.perf_counter()
    bfs_path, bfs_explored = solve_bfs(maze_bfs)
    bfs_time = (time.perf_counter() - t0) * 1000 # Convert to milliseconds
    
    print("-" * 50)
    
    # --- RUN A* ---
    maze_astar = Maze(maze_data["layout"])
    t0 = time.perf_counter()
    astar_path, astar_explored = solve_astar(maze_astar)
    astar_time = (time.perf_counter() - t0) * 1000 # Convert to milliseconds
    
    print("\n" + "="*60)
    print(" 📊 FINAL BENCHMARK RESULTS 📊 ")
    print("="*60)
    
    # Calculate exploration efficiency gain
    if bfs_explored and astar_explored:
        saved_tiles = len(bfs_explored) - len(astar_explored)
        efficiency_gain = (saved_tiles / len(bfs_explored)) * 100
    else:
        efficiency_gain = 0.0

    # Display side-by-side comparison table
    print(f"{'Metric':<25} | {'BFS (Blind)':<15} | {'A* (Heuristic)':<15}")
    print("-" * 60)
    print(f"{'Path Length Found':<25} | {len(bfs_path):<15} | {len(astar_path):<15}")
    print(f"{'Tiles Explored (Memory)':<25} | {len(bfs_explored):<15} | {len(astar_explored):<15}")
    print(f"{'Execution Time (ms)':<25} | {bfs_time:<15.4f} | {astar_time:<15.4f}")
    print("-" * 60)
    
    if len(bfs_path) == len(astar_path):
        print("🤝 OPTIMALITY: Both algorithms found the exact same shortest path length!")
    
    print(f"💡 EFFICIENCY: A* explored {efficiency_gain:.1f}% fewer tiles than BFS by using math!")
    print("="*60)
    
    print("\nVisualizing A* Winning Path:")
    maze_astar.render(path=astar_path, visited=astar_explored)
    input("\nPress Enter to return to the main menu...")

def play_human_mode(maze_data):
    """
    Interactive mode where the human player navigates the maze using WASD keys
    and competes against the AI's optimal step count!
    """
    maze = Maze(maze_data["layout"])
    
    # First, let's run BFS silently in the background to get the true mathematical shortest path
    ai_path, _ = solve_bfs(maze)
    optimal_steps = len(ai_path) if ai_path else 0
    
    current_pos = maze.start
    player_path = [current_pos]
    
    print(f"\n" + "🎮"*30)
    print(f" HUMAN CHALLENGE: [{maze_data['name']}] ")
    print("🎮"*30)
    print(f"💡 The BFS AI solved this map in exactly {optimal_steps} steps.")
    print("🎯 Your goal: Reach the finish line (🏁) in as few steps as possible!")
    print("🕹️  Controls: Type W (Up), S (Down), A (Left), or D (Right) and press ENTER.")
    print("   Type Q to quit back to menu.")
    
    # Mapping WASD strings to coordinate changes: (row_change, col_change)
    moves = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1)
    }
    
    while True:
        # Render the maze showing the player's path so far as golden stars (⭐)
        maze.render(path=player_path)
        print(f"👣 Current Steps Taken: {len(player_path)} | Target AI Score: {optimal_steps}")
        
        if current_pos == maze.end:
            print("\n" + "🏆"*30)
            print(" CONGRATULATIONS! YOU ESCAPED THE LABYRINTH! ")
            print("🏆"*30)
            human_steps = len(player_path)
            print(f"👤 Your Total Steps:  {human_steps}")
            print(f"🤖 AI Optimal Steps:  {optimal_steps}")
            
            if human_steps == optimal_steps:
                print("🌟 ABSOLUTE PERFECTION! You matched the AI's shortest path exactly!")
            elif human_steps < optimal_steps:
                # Mathematically impossible unless there's a bug, but fun Easter egg!
                print("🤯 INCREDIBLE! You somehow beat the AI!")
            else:
                extra = human_steps - optimal_steps
                print(f"💡 Good run! But you took {extra} extra step(s) compared to the BFS algorithm.")
            print("="*60)
            break
            
        move_input = input("Enter move (W/A/S/D): ").strip().lower()
        
        if move_input == "q":
            print("\n👋 Giving up? Returning to main menu...")
            break
            
        if move_input not in moves:
            print("❌ Invalid control! Please use W, A, S, or D.")
            continue
            
        # Calculate the intended destination coordinate
        dr, dc = moves[move_input]
        r, c = current_pos
        new_r, new_c = r + dr, c + dc
        new_pos = (new_r, new_c)
        
        # Check boundary conditions and wall collisions
        if 0 <= new_r < maze.rows and 0 <= new_c < maze.cols:
            if maze.grid[new_r][new_c] == "█":
                print("💥 OUCH! You walked straight into a brick wall! Try another direction.")
            else:
                # Valid move! Update player position
                current_pos = new_pos
                player_path.append(current_pos)
        else:
            print("🚫 You can't walk off the edge of the map!")
            
    input("\nPress Enter to return to the main menu...")

def main():
    """Main application loop."""
    current_maze = MAZES["2"] # Default maze
    
    while True:
        print_header()
        print(f"📍 Active Track: [{current_maze['name']}]")
        print("-" * 60)
        print("1. 🗺️  Change Maze Track")
        print("2. 🌊 Run Solo: Breadth-First Search (BFS)")
        print("3. 🧠 Run Solo: A* (A-Star) Heuristic Search")
        print("4. ⚔️  THE BENCHMARK RACE: BFS vs. A* Showdown")
        print("5. 🎮 PLAY HUMAN MODE: Walk the Maze Yourself (WASD)")
        print("6. 🚪 Exit Suite")
        
        choice = input("\nEnter console command (1-6): ").strip()
        
        if choice == "1":
            current_maze = select_maze()
            print(f"✅ Track switched to: {current_maze['name']}")
        elif choice == "2":
            run_individual_test("BFS", current_maze)
        elif choice == "3":
            run_individual_test("A*", current_maze)
        elif choice == "4":
            run_benchmark_race(current_maze)
        elif choice == "5":
            play_human_mode(current_maze)
        elif choice == "6":
            print("\n👋 Shutting down AI Racing Console. Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid selection! Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()