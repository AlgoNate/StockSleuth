import os
import json
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"

# Ensure watchlist exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Example list of symbols
symbols_to_check = [
    "GME", "AMC", "PLUG", "NOK", "SNDL", "VKSC", "UCLE", "PPCB",
    "BIEL", "CYAN", "GLNLF", "CPMD", "DMIFF", "NRXPW", "IDGC",
    "VHAI", "ARRRF", "BFYW", "ANORF", "AMHGQ"
]

penny_stocks = []

print("🔎 Scanning symbols for penny stocks (price <= $1)...")

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({"symbol": symbol, "name": name, "price": price})
                print(f"✅ {symbol} added: ${price}")
    except Exception as e:
        print(f"⚠️ Could not fetch {symbol}: {e}")

# Save watchlist.json
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"✅ Watchlist generated with {len(penny_stocks)} penny stocks.")
