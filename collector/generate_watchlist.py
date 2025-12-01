import os
import json
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"

# Ensure watchlist file exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Hardcoded list of potential penny stocks
symbols_to_check = [
    "GME", "AMC", "PLUG", "NOK", "SNDL", "VKSC", "UCLE", "PPCB",
    "BIEL", "CYAN", "GLNLF", "CPMD", "DMIFF", "NRXPW", "IDGC",
    "VHAI", "ARRRF", "BFYW", "ANORF", "AMHGQ"
]

penny_stocks = []

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:  # Only penny stocks
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({"symbol": symbol, "name": name, "price": price})
    except:
        continue

# Save watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"✅ Watchlist generated with {len(penny_stocks)} penny stocks")
