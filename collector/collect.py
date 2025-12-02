import os
import json
from datetime import datetime
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_FILE = "collector/daily_stock_data.json"

# Ensure watchlist file exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Example symbols; can also load dynamically from watchlist
symbols_to_check = ["GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
                    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
                    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"]

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:  # Penny stock filter
                name = ticker.info.get("shortName", symbol)
                percent_change = round((price - data["Close"].iloc[0])/data["Close"].iloc[0]*100, 2)
                penny_stocks.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(price, 3),
                    "percent_change": percent_change
                })
    except Exception as e:
        print(f"⚠️ Failed to fetch {symbol}: {e}")
        continue

# Update watchlist.json (symbol + name)
watchlist_data = [{"symbol": s["symbol"], "name": s["name"]} for s in penny_stocks]
with open(WATCHLIST_FILE, "w") as f:
    json.dump(watchlist_data, f, indent=2)

# Append daily data
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

print(f"✅ Collected {len(penny_stocks)} penny stocks")
