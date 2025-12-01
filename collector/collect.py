import os
import json
import requests
from datetime import datetime

# ------------------------
# File paths
# ------------------------
WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_FOLDER = "collector/history"

# ------------------------
# Finnhub API setup
# ------------------------
API_KEY = os.environ.get("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

# ------------------------
# Ensure necessary files/folders exist
# ------------------------
os.makedirs(HISTORY_FOLDER, exist_ok=True)

if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "w") as f:
        json.dump([], f)

# ------------------------
# Fetch all US stock symbols
# ------------------------
try:
    res = requests.get(f"{BASE_URL}/stock/symbol?exchange=US&token={API_KEY}")
    res.raise_for_status()
    all_stocks = res.json()
except Exception as e:
    print("❌ Error fetching US stock list:", e)
    all_stocks = []

# ------------------------
# Filter penny stocks (price <= $1)
# ------------------------
penny_stocks = []
for stock in all_stocks:
    symbol = stock.get("symbol")
    name = stock.get("description", "")
    try:
        price_res = requests.get(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price_res.raise_for_status()
        price_data = price_res.json()
        price = price_data.get("c", 0)
        if price <= 1 and price > 0:
            penny_stocks.append({"symbol": symbol, "name": name})
    except:
        continue

# Save updated watchlist.json
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"✅ Watchlist updated with {len(penny_stocks)} penny stocks.")

# ------------------------
# Collect daily stock data
# ------------------------
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in penny_stocks:
    symbol = stock["symbol"]
    name = stock["name"]
    try:
        price_res = requests.get(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price_res.raise_for_status()
        price_data = price_res.json()
        price = price_data.get("c", 0)
        prev_close = price_data.get("pc", 0)
        percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0
        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": percent_change
        })
    except:
        continue

# ------------------------
# Append to daily_stock_data.json
# ------------------------
with open(DAILY_DATA_FILE, "r") as f:
    data = json.load(f)

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Daily stock data updated at {daily_entry['timestamp']}")

# ------------------------
# Save historical snapshot
# ------------------------
timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
history_file = os.path.join(HISTORY_FOLDER, f"daily_stock_data_{timestamp}.json")

with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

print(f"✅ Saved historical snapshot to {history_file}")
