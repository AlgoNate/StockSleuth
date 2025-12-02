import os
import json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

# Ensure watchlist exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Sample symbols; extend as needed
symbols_to_check = ["GME", "AMC", "PLUG", "NOK", "SNDL"]

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1mo")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                # Add last 7 days closing prices as history
                history = list(data["Close"].tail(7))
                penny_stocks.append({
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "percent_change": round((price - data["Close"].iloc[-2]) / data["Close"].iloc[-2] * 100, 2) if len(data) > 1 else 0,
                    "history": history
                })
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Save daily data
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": penny_stocks
}

if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Save watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"✅ Daily data updated with {len(penny_stocks)} penny stocks.")
