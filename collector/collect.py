import os
import json
import requests
import logging
from datetime import datetime

# -------------------------------
#  LOGGING SETUP
# -------------------------------
LOG_FILE = "collector/collector.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("📌 Collector started")


WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

API_KEY = os.environ.get("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"


# -------------------------------
#  VALIDATE API KEY
# -------------------------------
if not API_KEY:
    msg = "❌ FINNHUB_API_KEY not found in environment variables!"
    print(msg)
    logging.error(msg)
    raise SystemExit(msg)

logging.info("API key detected. Starting operations...")


# -------------------------------
#  Ensure watchlist.json exists
# -------------------------------
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)
    logging.info("Created new empty watchlist.json")


# -------------------------------
#  Fetch all US stock symbols
# -------------------------------
logging.info("Fetching US stock list from Finnhub...")

try:
    res = requests.get(f"{BASE_URL}/stock/symbol?exchange=US&token={API_KEY}")
    res.raise_for_status()
    all_stocks = res.json()
    logging.info(f"Fetched {len(all_stocks)} US stock symbols")
except Exception as e:
    msg = f"❌ Error fetching US stock list: {e}"
    print(msg)
    logging.error(msg)
    all_stocks = []


# -------------------------------
#  Filter penny stocks
# -------------------------------
logging.info("Filtering penny stocks (price ≤ $1)...")

penny_stocks = []

for stock in all_stocks:
    symbol = stock.get("symbol")
    name = stock.get("description", "")

    try:
        price_res = requests.get(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price_data = price_res.json()
        price = price_data.get("c", 0)

        if 0 < price <= 1:
            penny_stocks.append({"symbol": symbol, "name": name})
            logging.info(f"Added penny stock: {symbol} at ${price}")

    except Exception as e:
        logging.warning(f"Skipping symbol {symbol}: {e}")
        continue

# Save watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

logging.info(f"Watchlist saved with {len(penny_stocks)} penny stocks.")


# -------------------------------
#  Collect daily stock data
# -------------------------------
logging.info("Collecting daily stock data...")

daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in penny_stocks:
    symbol = stock["symbol"]
    name = stock["name"]

    try:
        price_res = requests.get(f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}")
        price_data = price_res.json()

        price = price_data.get("c", 0)
        prev_close = price_data.get("pc", 0)

        pct_change = 0
        if prev_close:
            pct_change = round((price - prev_close) / prev_close * 100, 2)

        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": pct_change
        })

        logging.info(f"{symbol} → ${price} ({pct_change}%)")

    except Exception as e:
        logging.error(f"❌ Error fetching data for {symbol}: {e}")
        continue


# -------------------------------
#  Append to daily_stock_data.json
# -------------------------------
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

logging.info("Daily stock data entry saved")
logging.info("🎉 Collector completed successfully")
print(f"Daily stock data updated at {daily_entry['timestamp']}")
