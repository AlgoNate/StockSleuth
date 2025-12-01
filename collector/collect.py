import json
from datetime import datetime
import yfinance as yf
import os

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

# Ensure watchlist exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Load watchlist
with open(WATCHLIST_FILE) as f:
    watchlist = json.load(f)

# Collect daily stock data
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for symbol in watchlist:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice", 0)
        prev_close = info.get("previousClose", 0)
        percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0

        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": info.get("shortName", ""),
            "price": price,
            "percent_change": percent_change
        })
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        continue

# Append to daily_stock_data.json
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE) as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Daily stock data updated at {daily_entry['timestamp']}")
