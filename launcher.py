import os
import sys
import subprocess
import webbrowser
import time

def print_banner():
    """Prints the Master Arcade Hub ASCII banner."""
    print("\n" + "="*65)
    print(" 🎮  MULTI-PARADIGM SOFTWARE ENGINEERING ARCADE HUB  🎮 ")
    print("="*65)
    print(" ARCHITECTURE: JavaScript/React | Java OOP | Python Backend")
    print("="*65)

def run_react_game():
    """
    Handles frontend web applications. Because React dev servers run asynchronously 
    and block the terminal, we launch the browser and provide clean CLI instructions.
    """
    print("\n--- ⚛️  LAUNCHING GAME #1: REACT TIC-TAC-TOE ---")
    print("💡 Frontend web applications run inside a local Node.js server.")
    print("To play, open a new terminal window, navigate to the folder, and start the server:\n")
    print("   cd game1_tictactoe_react")
    print("   npm run dev   # (or 'npm start' depending on your bundler)")
    print("\n🌐 Attempting to open default development browser at http://localhost:5173 ...")
    time.sleep(1)
    # Open the browser automatically (Vite default is 5173, Create-React-App is 3000)
    webbrowser.open("http://localhost:5173")
    webbrowser.open("http://localhost:3000")
    input("\nPress Enter to return to the Master Menu...")

def run_java_game():
    """
    Compiles and executes Java bytecode programmatically using subprocess.
    """
    print("\n--- ☕ LAUNCHING GAME #2: JAVA BLACKJACK ---")
    java_dir = "game2_blackjack_java"
    
    if not os.path.exists(java_dir):
        print(f"❌ Error: Directory '{java_dir}' not found!")
        input("\nPress Enter to return to menu...")
        return

    print("⚙️  Invoking Java Compiler (javac)...")
    # 1. Compile the .java source code into a .class bytecode file
    compile_process = subprocess.run(
        ["javac", "Blackjack.java"], 
        cwd=java_dir, # Crucial: Run command inside the Java directory
        capture_output=True, 
        text=True
    )
    
    # Check exit code (0 means success in operating systems)
    if compile_process.returncode != 0:
        print("🚨 JAVA COMPILATION ERROR:")
        print(compile_process.stderr)
        input("\nPress Enter to return to menu...")
        return
        
    print("✅ Compilation successful! Spawning Java Virtual Machine (JVM)...\n")
    time.sleep(0.5)
    
    # 2. Execute the compiled Java bytecode
    subprocess.run(["java", "Blackjack"], cwd=java_dir)
    print("\n👋 JVM session ended.")
    input("\nPress Enter to return to the Master Menu...")

def run_python_game(folder_name, script_name="main.py", game_title=""):
    """
    Executes Python games in a separate child process while preserving their working directory.
    """
    print(f"\n--- 🐍 LAUNCHING: {game_title.upper()} ---")
    
    if not os.path.exists(folder_name):
        print(f"❌ Error: Directory '{folder_name}' not found!")
        input("\nPress Enter to return to menu...")
        return

    print(f"🚀 Spawning Python process inside '{folder_name}'...\n")
    time.sleep(0.5)
    
    # sys.executable guarantees we use the exact same Python interpreter running this hub
    subprocess.run([sys.executable, script_name], cwd=folder_name)
    
    print(f"\n👋 Closed {game_title}.")
    input("\nPress Enter to return to the Master Menu...")

def main():
    """Main application loop."""
    while True:
        print_banner()
        print("1. ⚛️  Game #1: Tic-Tac-Toe Arcade         [JavaScript / React UI]")
        print("2. ☕ Game #2: Console Blackjack            [Java / OOP Architecture]")
        print("3. 📈 Game #3: Live Crypto Tycoon          [Python / REST APIs & JSON]")
        print("4. 🕵️‍♂️ Game #4: Cyberpunk Hacker CTF        [Python / SQLite & Regex]")
        print("5. 🤖 Game #5: AI Maze Runner & Benchmark  [Python / Graph Algorithms]")
        print("6. 🚪 Exit Master Hub")
        print("-" * 65)
        
        choice = input("Select an application to boot (1-6): ").strip()
        
        if choice == "1":
            run_react_game()
        elif choice == "2":
            run_java_game()
        elif choice == "3":
            run_python_game("game3_stock_tycoon", "main.py", "Crypto Stock Tycoon")
        elif choice == "4":
            run_python_game("game4_cyberpunk_ctf", "main.py", "Cyberpunk Forensic CTF")
        elif choice == "5":
            run_python_game("game5_ai_maze_runner", "main.py", "AI Maze Runner")
        elif choice == "6":
            print("\n👋 Shutting down Master Arcade Hub. Keep coding!")
            sys.exit()
        else:
            print("❌ Invalid command! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()