import json
from pathlib import Path

WATCHLIST_FILE = Path("collector/watchlist.json")
DAILY_FILE = Path("collector/daily_stock_data.json")

# Load latest daily data
if DAILY_FILE.exists():
    with open(DAILY_FILE) as f:
        daily_data = json.load(f)
    latest_stocks = daily_data[-1]["stocks"] if daily_data else []
else:
    latest_stocks = []

# Filter penny stocks
penny_watchlist = [{"symbol": s["symbol"], "name": s["name"]} 
                   for s in latest_stocks if s["price"] <= 1]

# Save watchlist
WATCHLIST_FILE.parent.mkdir(exist_ok=True)
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_watchlist, f, indent=2)

print(f"✔ Watchlist updated ({len(penny_watchlist)} stocks)")
