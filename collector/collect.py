import os
import json
import finnhub
from datetime import datetime

API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise RuntimeError("FINNHUB_API_KEY not set in environment")

client = finnhub.Client(api_key=API_KEY)

# Example: list of penny tickers to track
tickers = ["AAPL", "TSLA", "GME", "PLUG"]  # Replace with your real list

results = []
for sym in tickers:
    try:
        quote = client.quote(sym)
        price = quote.get("c")
        prev_close = quote.get("pc")
        if price is None or prev_close is None:
            continue
        percent_change = (price - prev_close) / prev_close * 100

        profile = client.company_profile2(symbol=sym)
        name = profile.get("name") or sym

        results.append({
            "symbol": sym,
            "name": name,
            "price": price,
            "percent_change": percent_change,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        print("Error fetching for", sym, e)

with open("collector/daily_stock_data.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done — wrote", len(results), "stocks")
