# collector/collect.py
import os
import json
from datetime import datetime
import finnhub

API_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=API_KEY)

# Load the pre-generated watchlist
with open("collector/watchlist.json", "r") as f:
    watchlist = json.load(f)

top_stocks = []

for stock in watchlist:
    symbol = stock["symbol"]
    name = stock.get("name", symbol)
    try:
        quote = client.quote(symbol)
        current_price = quote["c"]
        prev_close = quote["pc"]

        if current_price == 0 or prev_close == 0:
            continue

        percent_change = (current_price - prev_close) / prev_close * 100

        # Filter: penny stock ≤ $1 and significant gain ≥10%
        if current_price <= 1 and percent_change >= 10:
            top_stocks.append({
                "symbol": symbol,
                "name": name,
                "price": round(current_price, 4),
                "percent_change": round(percent_change, 2)
            })

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Sort top movers descending by percent change
top_stocks.sort(key=lambda x: x["percent_change"], reverse=True)

# Keep top 25
top_stocks = top_stocks[:25]

# Add timestamp
output = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "stocks": top_stocks
}

# Save JSON
os.makedirs("collector", exist_ok=True)
with open("collector/daily_stock_data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(top_stocks)} top penny stocks to collector/daily_stock_data.json")
