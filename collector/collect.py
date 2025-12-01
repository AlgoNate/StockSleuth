import os
import json
from datetime import datetime
import yfinance as yf
import pandas as pd

# File paths
WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history/"

# Ensure watchlist.json exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Ensure history directory exists
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# Load watchlist
try:
    with open(WATCHLIST_FILE) as f:
        watchlist = json.load(f)
except:
    watchlist = []

# If watchlist is empty, populate with example penny stocks (or your logic)
if not watchlist:
    tickers = ["GME", "AMC", "PLUG", "NOK", "SNDL"]
    watchlist = [{"symbol": t, "name": t} for t in tickers]

# Save updated watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(watchlist, f, indent=2)

print(f"✅ Watchlist contains {len(watchlist)} stocks.")

# Collect daily stock data
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in watchlist:
    symbol = stock["symbol"]
    name = stock["name"]
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            close_price = float(data["Close"].iloc[-1])
            prev_close = float(data["Close"].iloc[-2]) if len(data) > 1 else close_price
            percent_change = round((close_price - prev_close) / prev_close * 100, 2) if prev_close else 0
            daily_entry["stocks"].append({
                "symbol": symbol,
                "name": name,
                "price": close_price,
                "percent_change": percent_change
            })
    except Exception as e:
        print(f"⚠️ Error fetching {symbol}: {e}")
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

# Optional: save a copy in history folder for backup
history_file = os.path.join(HISTORY_DIR, f"{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

print(f"✅ Daily stock data updated at {daily_entry['timestamp']}")
