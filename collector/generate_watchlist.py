import yfinance as yf
import json

WATCHLIST_FILE = "collector/watchlist.json"

# Example: top US penny stocks (symbols under $5)
symbols = ["GME", "PLUG", "AMC", "FUBO", "SNDL"]  # replace/add symbols you want

watchlist = []

for symbol in symbols:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice", 0)
        if price <= 5 and price > 0:
            watchlist.append(symbol)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        continue

# Save watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(watchlist, f, indent=2)

print(f"✅ Watchlist updated with {len(watchlist)} symbols")
