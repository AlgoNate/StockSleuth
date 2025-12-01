import os
import json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"

# Ensure watchlist.json exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Ensure history directory exists
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# Load watchlist
with open(WATCHLIST_FILE, "r") as f:
    watchlist = json.load(f)

if not watchlist:
    print("⚠️ Watchlist is empty. Run generate_watchlist.py first.")
    exit()

# Collect daily stock data
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in watchlist:
    symbol = stock["symbol"]
    name = stock.get("name", "")

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")  # last 2 days for percent change

        if data.empty:
            continue

        latest_close = data["Close"][-1]
        prev_close = data["Close"][-2] if len(data) > 1 else latest_close
        percent_change = round((latest_close - prev_close) / prev_close * 100, 2) if prev_close else 0

        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": round(latest_close, 2),
            "percent_change": percent_change
        })
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        continue

# Append to daily_stock_data.json
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Save to history file for backup
history_file = os.path.join(HISTORY_DIR, f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

print(f"✅ Daily stock data updated at {daily_entry['timestamp']}")
print(f"Saved backup to {history_file}")
