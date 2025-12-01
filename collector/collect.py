import os
import json
import logging
from datetime import datetime
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("collector.log"),
        logging.StreamHandler()
    ]
)

# ----------------------------
# Constants & environment
# ----------------------------
WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_FOLDER = "collector/history"

API_KEY = os.environ.get("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

# Ensure necessary folders exist
os.makedirs(HISTORY_FOLDER, exist_ok=True)

# Ensure watchlist.json exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# ----------------------------
# Functions
# ----------------------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_json(url):
    """Fetch JSON data from URL with retries."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# ----------------------------
# Fetch all US stock symbols
# ----------------------------
try:
    all_stocks = fetch_json(f"{BASE_URL}/stock/symbol?exchange=US&token={API_KEY}")
    logging.info(f"Fetched {len(all_stocks)} US stock symbols")
except Exception as e:
    logging.error(f"Error fetching US stock list: {e}")
    all_stocks = []

# ----------------------------
# Filter penny stocks (price <= $1)
# ----------------------------
penny_stocks = []
for stock in all_stocks:
    symbol = stock.get("symbol")
    name = stock.get("description", "")
    try:
        price_data = fetch_json(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price = price_data.get("c", 0)
        if 0 < price <= 1:
            penny_stocks.append({"symbol": symbol, "name": name})
    except Exception as e:
        logging.warning(f"Failed to fetch price for {symbol}: {e}")
        continue

# Save watchlist.json
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)
logging.info(f"Watchlist updated with {len(penny_stocks)} penny stocks")

# ----------------------------
# Collect daily stock data
# ----------------------------
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in penny_stocks:
    symbol = stock["symbol"]
    name = stock["name"]
    try:
        price_data = fetch_json(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price = price_data.get("c", 0)
        prev_close = price_data.get("pc", 0)
        percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0
        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": percent_change
        })
    except Exception as e:
        logging.warning(f"Failed to fetch daily data for {symbol}: {e}")
        continue

# ----------------------------
# Append to daily_stock_data.json
# ----------------------------
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)
logging.info(f"Daily stock data updated at {daily_entry['timestamp']}")

# ----------------------------
# Save historical snapshot
# ----------------------------
timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
history_file = os.path.join(HISTORY_FOLDER, f"daily_stock_data_{timestamp}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)
logging.info(f"Saved historical snapshot to {history_file}")
