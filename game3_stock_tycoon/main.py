import sys
# 1. Importing our custom modules just like standard Python libraries!
from market import get_live_prices
from portfolio import load_game, save_game

def display_dashboard(player_data, prices):
    """Calculates live net worth and displays the player's dashboard."""
    print("\n" + "="*50)
    print(" 📈 LIVE CRYPTO TYCOON TERMINAL 📈 ")
    print("="*50)
    
    cash = player_data["cash"]
    print(f"💵 Available Cash:  ${cash:,.2f}")
    print("-" * 50)
    print("🪙 YOUR PORTFOLIO & LIVE VALUATION:")
    
    total_crypto_value = 0.0
    
    # Check if we successfully pulled live prices from the internet
    if prices:
        for coin, amount in player_data["portfolio"].items():
            live_price = prices.get(coin, {}).get("usd", 0.0)
            coin_val = amount * live_price
            total_crypto_value += coin_val
            print(f"  • {coin.capitalize():<10}: {amount:>8.4f} owned | Live Price: ${live_price:>10,.2f} | Value: ${coin_val:>10,.2f}")
    else:
        print("  ⚠️ Live market offline! Showing quantities only:")
        for coin, amount in player_data["portfolio"].items():
            print(f"  • {coin.capitalize():<10}: {amount:>8.4f} owned")
            
    net_worth = cash + total_crypto_value
    print("-" * 50)
    print(f"🏆 TOTAL NET WORTH: ${net_worth:,.2f}")
    print("="*50)

def buy_crypto(player_data, prices):
    """Handles the logic and math for purchasing cryptocurrency."""
    if not prices:
        print("🚨 Cannot buy while live market connection is offline!")
        return

    print("\n--- 🛒 BUY CRYPTO ---")
    print("Available Coins: 1. Bitcoin | 2. Ethereum | 3. Solana")
    choice = input("Enter coin name (e.g., bitcoin): ").lower().trim() if hasattr(input(""), 'trim') else input("Enter coin name (e.g., bitcoin): ").lower().strip()
    
    if choice not in player_data["portfolio"]:
        print("❌ Invalid coin choice!")
        return

    live_price = prices[choice]["usd"]
    print(f"💡 {choice.capitalize()} is currently trading at ${live_price:,.2f}")
    
    try:
        spend_amount = float(input(f"How much USD do you want to spend? (Max: ${player_data['cash']:,.2f}): $"))
        
        if spend_amount <= 0:
            print("❌ Amount must be greater than $0!")
            return
        if spend_amount > player_data["cash"]:
            print("❌ Insufficient funds!")
            return
            
        # Calculate how many coins they get for their USD
        coins_bought = spend_amount / live_price
        
        # Execute trade
        player_data["cash"] -= spend_amount
        player_data["portfolio"][choice] += coins_bought
        player_data["history"].append(f"BOUGHT {coins_bought:.4f} {choice.capitalize()} for ${spend_amount:,.2f}")
        
        # Save immediately after a successful trade
        save_game(player_data)
        print(f"✅ SUCCESS! Bought {coins_bought:.4f} {choice.capitalize()}!")
        
    except ValueError:
        print("❌ Invalid number entered! Please enter numeric values only.")

def sell_crypto(player_data, prices):
    """Handles the logic and math for selling cryptocurrency."""
    if not prices:
        print("🚨 Cannot sell while live market connection is offline!")
        return

    print("\n--- 💰 SELL CRYPTO ---")
    choice = input("Enter coin name to sell (e.g., bitcoin): ").lower().strip()
    
    if choice not in player_data["portfolio"]:
        print("❌ Invalid coin choice!")
        return

    owned = player_data["portfolio"][choice]
    if owned <= 0:
        print(f"❌ You don't own any {choice.capitalize()}!")
        return

    live_price = prices[choice]["usd"]
    print(f"💡 You own {owned:.4f} {choice.capitalize()} (Worth: ${owned * live_price:,.2f})")
    
    try:
        sell_coins = float(input(f"How many coins do you want to sell? (Max: {owned:.4f}): "))
        
        if sell_coins <= 0:
            print("❌ Amount must be greater than 0!")
            return
        if sell_coins > owned:
            print("❌ You can't sell more coins than you own!")
            return
            
        # Calculate USD gained
        usd_gained = sell_coins * live_price
        
        # Execute trade
        player_data["portfolio"][choice] -= sell_coins
        player_data["cash"] += usd_gained
        player_data["history"].append(f"SOLD {sell_coins:.4f} {choice.capitalize()} for ${usd_gained:,.2f}")
        
        # Save immediately after a successful trade
        save_game(player_data)
        print(f"✅ SUCCESS! Sold {sell_coins:.4f} {choice.capitalize()} for ${usd_gained:,.2f}!")
        
    except ValueError:
        print("❌ Invalid number entered! Please enter numeric values only.")

def main():
    """Main application loop."""
    print("🚀 Booting up Crypto Tycoon Terminal...")
    player_data = load_game()
    prices = get_live_prices()

    while True:
        display_dashboard(player_data, prices)
        
        print("\n--- TERMINAL MENU ---")
        print("1. 🔄 Refresh Live Market Prices")
        print("2. 🛒 Buy Crypto")
        print("3. 💰 Sell Crypto")
        print("4. 📜 View Transaction History")
        print("5. 🚪 Save & Exit")
        
        choice = input("\nEnter your command (1-5): ").strip()
        
        if choice == "1":
            print("\n🌐 Fetching latest market prices from CoinGecko...")
            prices = get_live_prices()
        elif choice == "2":
            buy_crypto(player_data, prices)
        elif choice == "3":
            sell_crypto(player_data, prices)
        elif choice == "4":
            print("\n--- 📜 TRANSACTION HISTORY ---")
            if not player_data["history"]:
                print("No transactions yet. Start trading!")
            else:
                for log in player_data["history"][-10:]: # Show last 10 trades
                    print(f"  • {log}")
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            save_game(player_data)
            print("\n👋 Thanks for playing! Portfolio saved. Exiting terminal...")
            sys.exit()
        else:
            print("❌ Invalid command! Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()