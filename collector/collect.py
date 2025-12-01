import os
import json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

# Load watchlist
if os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE) as f:
        symbols_to_check = [stock["symbol"] for stock in json.load(f)]
else:
    symbols_to_check = ["PLUG", "GME", "AMC"]  # fallback symbols

# Collect daily stock data
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
    except Exception as e:
        print(f"⚠️ Could not fetch {symbol}: {e}")

# Load previous JSON
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE) as f:
        all_data = json.load(f)
else:
    all_data = []

# Append new entry
all_data.append(daily_entry)

# Save back
with open(DAILY_DATA_FILE, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"✅ Daily stock data updated with {len(daily_entry['stocks'])} stocks.")
