import os
import json
from datetime import datetime
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_FILE = "collector/daily_stock_data.json"

# Ensure watchlist exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Define your symbols list — you can adjust as you need
symbols_to_check = [
    "GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"
]

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            # Only consider penny stocks (<= 1 USD, > 0)
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                # Compute percent_change against previous close if possible
                prev_close = float(data["Close"].iloc[0])
                if prev_close:
                    percent_change = round((price - prev_close) / prev_close * 100, 2)
                else:
                    percent_change = 0.0
                penny_stocks.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(price, 6),
                    "percent_change": percent_change
                })
    except Exception as e:
        # optional: log or print error
        continue

# Save watchlist (symbol + name only)
with open(WATCHLIST_FILE, "w") as f:
    json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in penny_stocks], f, indent=2)

# Prepare daily entry
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": penny_stocks
}

# Load existing data or start fresh
if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE) as f:
        existing = json.load(f)
else:
    existing = []

existing.append(daily_entry)

# Write full data back
with open(DAILY_FILE, "w") as f:
    json.dump(existing, f, indent=2)

print(f"✅ Collected {len(penny_stocks)} penny stocks — JSON updated.")
