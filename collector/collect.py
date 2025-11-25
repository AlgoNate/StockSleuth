# collector/collect.py
import os
import json
from datetime import datetime
import finnhub

API_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=API_KEY)

WATCHLIST_FILE = "collector/watchlist.json"
OUTPUT_FILE = "collector/daily_stock_data.json"

# Load the watchlist
with open(WATCHLIST_FILE, "r") as f:
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
top_stocks = top_stocks[:25]  # Keep top 25

# Add timestamp
timestamp = datetime.utcnow().isoformat() + "Z"
run_data = {
    "timestamp": timestamp,
    "stocks": top_stocks
}

# Ensure collector folder exists
os.makedirs("collector", exist_ok=True)

# Load existing history if exists
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        history = json.load(f)
else:
    history = []

# Append this run
history.append(run_data)

# Keep only last 7 days (optional)
# history = [h for h in history if datetime.fromisoformat(h["timestamp"][:-1]) > datetime.utcnow() - timedelta(days=7)]

# Save full history
with open(OUTPUT_FILE, "w") as f:
    json.dump(history, f, indent=2)

print(f"Saved top 25 penny stocks for {timestamp} to {OUTPUT_FILE}")
