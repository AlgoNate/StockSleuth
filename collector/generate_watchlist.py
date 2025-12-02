import json
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"

# Example symbols
symbols = [
    "GME", "AMC", "PLUG", "NOK", "SNDL",
    "VKSC", "UCLE", "PPCB", "BIEL",
    "CYAN", "GLNLF", "CPMD", "DMIFF",
    "NRXPW", "IDGC", "VHAI", "ARRRF",
    "BFYW", "ANORF", "AMHGQ"
]

penny_stocks = []

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({
                    "symbol": symbol,
                    "name": name
                })
    except Exception:
        continue

with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print("✔ Watchlist updated.")
