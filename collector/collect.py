import os
import json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"

# Ensure history directory exists
os.makedirs(HISTORY_DIR, exist_ok=True)

# Load watchlist
if os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE) as f:
        watchlist = json.load(f)
else:
    watchlist = []

symbols_to_check = [s["symbol"] for s in watchlist]

daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            name = ticker.info.get("shortName", symbol)
            daily_entry["stocks"].append({
                "symbol": symbol,
                "name": name,
                "price": price
            })
    except Exception:
        continue

# Append to main file
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE) as f:
        existing = json.load(f)
else:
    existing = []

existing.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(existing, f, indent=2)

# Save daily history copy
history_file = f"{HISTORY_DIR}/{daily_entry['timestamp'].replace(':', '-')}.json"
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

print("✔ Daily stock data updated.")
