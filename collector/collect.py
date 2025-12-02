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

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if hist.shape[0] >= 2:
            price = float(hist["Close"].iloc[-1])
            prev_close = float(hist["Close"].iloc[-2])
        elif hist.shape[0] == 1:
            price = float(hist["Close"].iloc[-1])
            prev_close = price
        else:
            # No data, skip 
            continue

        if 0 < price <= 1:
            name = ticker.info.get("shortName", symbol)
            # compute percent change safely
            if prev_close:
                percent_change = round((price - prev_close) / prev_close * 100, 2)
            else:
                percent_change = 0.0

            penny_stocks.append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "percent_change": percent_change
            })
    except Exception:
        continue

# Save watchlist (symbol + name) if desired
with open(WATCHLIST_FILE, "w") as f:
    json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in penny_stocks], f, indent=2)

# Build daily entry
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": penny_stocks
}

if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE) as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Collected {len(penny_stocks)} penny stocks. JSON updated.")
