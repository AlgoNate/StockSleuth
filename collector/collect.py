import os
import json
from datetime import datetime
import finnhub

# Initialize Finnhub client
API_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=API_KEY)

# Pre-filtered penny stock watchlist
# You can expand this to ~50–200 tickers
watchlist = [
    {"symbol": "SNDL", "description": "Sundial Growers"},
    {"symbol": "PLUG", "description": "Plug Power"},
    {"symbol": "FUV", "description": "Arcimoto, Inc."},
    {"symbol": "ZNGA", "description": "Zynga Inc"},
    {"symbol": "AAPL", "description": "Apple Inc."}  # example large-cap for testing
]

top_stocks = []

for stock in watchlist:
    symbol = stock["symbol"]
    name = stock["description"]
    try:
        quote = client.quote(symbol)
        open_price = quote["o"]
        current_price = quote["c"]
        prev_close = quote["pc"]
        
        # Skip if no valid prices
        if open_price == 0 or current_price == 0 or prev_close == 0:
            continue
        
        percent_change = (current_price - prev_close) / prev_close * 100
        
        # Filter: penny stock (<$1) and significant gain (>10%)
        if current_price < 1 and percent_change >= 10:
            top_stocks.append({
                "symbol": symbol,
                "name": name,
                "price": round(current_price, 4),
                "percent_change": round(percent_change, 2)
            })
            
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Sort descending by percent change
top_stocks.sort(key=lambda x: x["percent_change"], reverse=True)

# Keep only top 25
top_stocks = top_stocks[:25]

# Include timestamp
output = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "stocks": top_stocks
}

# Save JSON file
output_path = "collector/daily_stock_data.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(top_stocks)} top penny stocks to {output_path}")
