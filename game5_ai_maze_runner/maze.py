import time

# Built-in maze layouts of varying difficulty
MAZES = {
    "1": {
        "name": "The Rookie Loop",
        "layout": [
            "████████████████████",
            "█S  █        █     █",
            "█ █ █ ██████ █ ███ █",
            "█ █ █      █ █   █ █",
            "█ ████████ █ ███ █ █",
            "█          █     █E█",
            "████████████████████"
        ]
    },
    "2": {
        "name": "The Cyber Labyrinth",
        "layout": [
            "██████████████████████████",
            "█S       █               █",
            "██████ █ █ █████████████ █",
            "█      █ █ █           █ █",
            "█ ██████ █ █ █████████ █ █",
            "█ █    █   █ █       █ █ █",
            "█ █ ██ █████ █ █████ █ █ █",
            "█ █  █       █     █ █   █",
            "█ ████████████████ █ █████",
            "█                  █    E█",
            "██████████████████████████"
        ]
    }
}

class Maze:
    def __init__(self, layout):
        """Initializes the 2D grid and locates Start (S) and End (E) coordinates."""
        self.grid = layout
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.start = None
        self.end = None
        
        # Scan the 2D matrix to find (row, col) coordinates for Start and End
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "S":
                    self.start = (r, c)
                elif self.grid[r][c] == "E":
                    self.end = (r, c)
                    
        if not self.start or not self.end:
            raise ValueError("Maze layout must contain both 'S' (Start) and 'E' (End)!")

    def get_neighbors(self, pos):
        """
        Returns a list of valid adjacent (row, col) coordinates (Up, Down, Left, Right)
        that are NOT walls ('█'). This is the core of Graph Theory exploration!
        """
        r, c = pos
        neighbors = []
        
        # 4 Cardinal Directions: (row_change, col_change)
        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check boundary conditions and wall collisions
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != "█":
                    neighbors.append((nr, nc))
                    
        return neighbors

    def render(self, path=None, visited=None):
        """
        Prints the maze cleanly to the terminal.
        Can dynamically overlay the AI's visited nodes and final winning path!
        """
        path = set(path) if path else set()
        visited = set(visited) if visited else set()
        
        print()
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                pos = (r, c)
                char = self.grid[r][c]
                
                if pos == self.start:
                    row_str += "🟢" # Start
                elif pos == self.end:
                    row_str += "🏁" # End
                elif pos in path:
                    row_str += "⭐" # The winning AI path!
                elif pos in visited:
                    row_str += "░░" # Nodes explored by the AI
                elif char == "█":
                    row_str += "██" # Wall
                else:
                    row_str += "  " # Open space
            print(row_str)
        print()

# --- TESTING THE GRID ENGINE ---
if __name__ == "__main__":
    print("--- 🧪 TESTING MAZE GRAPH ENGINE ---")
    test_data = MAZES["1"]
    print(f"Loading Maze: {test_data['name']}")
    
    maze = Maze(test_data["layout"])
    print(f"Grid Size: {maze.rows}x{maze.cols}")
    print(f"Start Coordinate: {maze.start}")
    print(f"End Coordinate:   {maze.end}")
    
    # Test neighbor discovery from the Starting point
    start_neighbors = maze.get_neighbors(maze.start)
    print(f"Valid moves from Start {maze.start}: {start_neighbors}")
    
    # Render raw maze
    maze.render()