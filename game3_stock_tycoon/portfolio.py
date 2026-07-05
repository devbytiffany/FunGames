import json

# The default file name where our data will live on the hard drive
SAVE_FILE = "save_game.json"

def get_default_save():
    """Returns a fresh starting state for a brand new player."""
    return {
        "cash": 10000.0,
        "portfolio": {
            "bitcoin": 0.0,
            "ethereum": 0.0,
            "solana": 0.0
        },
        "history": []
    }

def load_game(filename=SAVE_FILE):
    """
    Attempts to load the game state from disk. 
    If the file doesn't exist or is corrupted, it returns a fresh account.
    """
    try:
        # Open the file in 'r' (read-only) mode
        with open(filename, "r") as file:
            data = json.load(file)
            print("📁 Game loaded successfully from disk!")
            return data
            
    except FileNotFoundError:
        # This triggers the very first time the player runs the game
        print("🆕 No save file found. Creating a new account with $10,000!")
        default_data = get_default_save()
        save_game(default_data, filename) # Create the file immediately
        return default_data
        
    except json.JSONDecodeError:
        # This triggers if someone opened the save file and messed up the formatting
        print("⚠️ Save file corrupted! Starting fresh with default account.")
        return get_default_save()

def save_game(data, filename=SAVE_FILE):
    """Writes the current Python dictionary directly to disk as a JSON file."""
    try:
        # Open the file in 'w' (write) mode — overwrites existing data
        with open(filename, "w") as file:
            # indent=4 formats the JSON file with clean line breaks so humans can read it
            json.dump(data, file, indent=4)
        print("💾 Portfolio safely saved to disk!")
        return True
    except IOError as e:
        print(f"🚨 Failed to save game: {e}")
        return False

# --- TESTING THE ENGINE ---
if __name__ == "__main__":
    print("--- 🧪 TESTING LOAD ENGINE ---")
    my_data = load_game()
    print(f"Current Balance: ${my_data['cash']:,.2f}")
    print(f"Current BTC Owned: {my_data['portfolio']['bitcoin']}")
    
    # Simulate a player buying 0.5 Bitcoin
    print("\n--- 🛒 SIMULATING A PURCHASE ---")
    print("Spending $30,000 to buy 0.5 BTC...")
    my_data["cash"] -= 30000.0
    my_data["portfolio"]["bitcoin"] += 0.5
    my_data["history"].append("Bought 0.5 BTC for $30,000")
    
    # Save the modifications back to disk
    print("\n--- 🧪 TESTING SAVE ENGINE ---")
    save_game(my_data)