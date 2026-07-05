import requests
import json

def get_live_prices():
    """
    Fetches real-time cryptocurrency prices from the web using a REST API.
    Returns a Python dictionary with the prices in USD.
    """
    # 1. The API endpoint URL (asking for Bitcoin, Ethereum, and Solana prices in USD)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
    
    try:
        print("🌐 Connecting to live market server...")
        # 2. Make an HTTP GET request to the server
        response = requests.get(url, timeout=5)
        
        # 3. Check if the server responded successfully (Status Code 200 = OK)
        if response.status_code == 200:
            # 4. Parse the JSON response into a native Python dictionary
            data = response.json()
            return data
        else:
            print(f"⚠️ Server error! Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        # This catches errors if your internet is down or the site is blocked
        print(f"🚨 Network error: {e}")
        return None

# --- TESTING OUR ENGINE ---
if __name__ == "__main__":
    prices = get_live_prices()
    
    if prices:
        print("\n--- 📊 LIVE MARKET DATA ---")
        # Pretty-print the raw JSON dictionary so we can see its structure
        print(json.dumps(prices, indent=4))
        
        # Extracting specific numbers from the dictionary:
        btc_price = prices["bitcoin"]["usd"]
        print(f"\n💡 Right now, 1 Bitcoin is worth ${btc_price:,.2f} USD!")
        