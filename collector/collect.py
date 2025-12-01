import os
import json
from datetime import datetime
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

# Load watchlist
if os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE) as f:
        watchlist = json.load(f)
else:
    watchlist = []

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
            price = float(data["Close"].iloc[-1])
            prev_close = float(data["Close"].iloc[-2]) if len(data) > 1 else price
            percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0
            daily_entry["stocks"].append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "percent_change": percent_change
            })
    except Exception as e:
        print(f"⚠️ Could not fetch {symbol}: {e}")

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
