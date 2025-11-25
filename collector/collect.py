import os
import json
import finnhub
from datetime import datetime

# Load API key from GitHub Actions secret
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise Exception("FINNHUB_API_KEY environment variable not set")

client = finnhub.Client(api_key=API_KEY)

print("Fetching full US stock list…")

# 1. Get ALL US stock symbols from Finnhub
try:
    all_stocks = client.stock_symbols("US")
except Exception as e:
    print("Error fetching US stock list:", e)
    raise

results = []

print(f"Total symbols returned: {len(all_stocks)}")
print("Filtering for penny stocks…")

for stock in all_stocks:
    symbol = stock.get("symbol")
    name = stock.get("description", "")

    # Skip symbols with '.' (preferred classes, ETFs, etc.)
    if "." in symbol:
        continue

    try:
        quote = client.quote(symbol)
        price = quote.get("c")      # current price
        prev_close = quote.get("pc")  # previous close

        if price is None or prev_close in (None, 0):
            continue

        percent_change = (price - prev_close) / prev_close * 100

        # FILTER RULES:
        # 1. Price must be under $1.00
        # 2. Percent change must be above +10%
        if price < 1 and percent_change > 10:
            results.append({
                "symbol": symbol,
                "name": name,
                "price": round(price, 4),
                "percent_change": percent_change,
                "timestamp": datetime.utcnow().isoformat()
            })

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        continue

# Sort stoc
