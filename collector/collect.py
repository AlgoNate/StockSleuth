import os
import json
import finnhub
from datetime import datetime

API_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=API_KEY)

# 1. Get ALL US Stocks
all_stocks = client.stock_symbols("US")

results = []

for stock in all_stocks:
    symbol = stock.get("symbol")
    name = stock.get("description", "")

    # Skip ETFs and symbols with weird formats
    if "." in symbol:
        continue  

    try:
        quote = client.quote(symbol)

        price = quote.get("c")          # current price
        prev = quote.get("pc")         # previous close

        # skip if missing data
        if price is None or prev is None or prev == 0:
            continue

        percent = (price - prev) / prev * 100

        # FILTER RULES:
        if price < 1 and percent > 10:
            results.append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "percent_change": percent,
                "timestamp": datetime.utcnow().isoformat()
            })

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Sort top 25 by percent change descending
results = sorted(results, key=lambda x: x["percent_change"], reverse=True)[:25]

# Save output
with open("collector/daily_stock_data.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved", len(results), "top penny stocks.")
