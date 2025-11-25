# collector/generate_watchlist.py
import yfinance as yf
import pandas as pd
import json
import os

os.makedirs("collector", exist_ok=True)

# Download NASDAQ-listed tickers CSV
tickers = pd.read_csv("https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv")

penny_stocks = []

for symbol in tickers['Symbol']:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if hist.empty:
            continue
        price = hist['Close'][-1]
        if price <= 1:
            penny_stocks.append({"symbol": symbol, "name": stock.info.get("shortName", symbol)})
    except:
        continue

# Save watchlist
with open("collector/watchlist.json", "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"Watchlist generated: {len(penny_stocks)} penny stocks")
