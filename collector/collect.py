import os, json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_FILE = "collector/daily_stock_data.json"

if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

symbols_to_check = ["GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE"]

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "percent_change": round((price - data["Close"].iloc[0])/data["Close"].iloc[0]*100,2)
                })
    except:
        continue

with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

# Append to daily data
daily_entry = {"timestamp": datetime.utcnow().isoformat(), "stocks": penny_stocks}

if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE) as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Collected {len(penny_stocks)} penny stocks")
