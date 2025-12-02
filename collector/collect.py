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
        if hist.empty or "Close" not in hist.columns:
            continue

        price = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2]) if hist.shape[0] >= 2 else price

        if not (0 < price <= 1):
            continue

        name = ticker.info.get("shortName", symbol)
        percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0.0

        results.append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": percent_change
        })

    except Exception:
        continue

# Optionally update watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in results], f, indent=2)

daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": results
}

if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE) as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Collected {len(results)} penny stocks — JSON updated.")
