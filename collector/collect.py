# File: collector/collect.py

import os
import json
from datetime import datetime
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_FILE = "collector/daily_stock_data.json"

symbols_to_check = [
    "GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"
]

results = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d", auto_adjust=False)

        # Skip if no data
        if hist.empty or "Close" not in hist.columns:
            continue

        # Latest close price
        price = float(hist["Close"].iloc[-1])

        # previous close (if exists)
        if hist.shape[0] >= 2:
            prev_close = float(hist["Close"].iloc[-2])
        else:
            prev_close = price

        # Only include penny stocks
        if not (0 < price <= 1):
            continue

        name = ticker.info.get("shortName", symbol)

        # compute percent change; avoid divide by zero
        if prev_close:
            percent_change = round((price - prev_close) / prev_close * 100, 2)
        else:
            percent_change = 0.0

        # Build stock object, always includes percent_change
        stock_obj = {
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": percent_change
        }
        results.append(stock_obj)

    except Exception:
        # If any exception, skip symbol
        continue

# Optionally update watchlist.json (just symbol + name)
with open(WATCHLIST_FILE, "w") as f:
    json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in results], f, indent=2)

# Build daily entry
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": results
}

# Load existing data (or start new)
if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

# Write updated JSON
with open(DAILY_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Collected {len(results)} penny stocks — JSON updated.")
