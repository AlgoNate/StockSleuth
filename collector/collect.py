import os
import json
import logging
from datetime import datetime
import yfinance as yf
import pandas as pd

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

# -------------------------------
#  FILE PATHS
# -------------------------------
WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"

# -------------------------------
#  Ensure watchlist.json exists
# -------------------------------
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)
    logging.info("Created new empty watchlist.json")

# -------------------------------
#  Fetch all US tickers (penny stock filter)
# -------------------------------
logging.info("Fetching US tickers and filtering penny stocks...")

try:
    # Example: S&P 500 tickers or custom list; here we'll use a simple predefined sample
    # Replace with your own symbols for full coverage if needed
    all_symbols = ["AAPL", "MSFT", "TSLA", "GME", "AMC", "NOK", "BB", "F"]
    
    penny_stocks = []
    
    for symbol in all_symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.info.get("regularMarketPrice", 0)
            name = ticker.info.get("shortName", symbol)
            
            if 0 < price <= 5:  # Adjust ceiling for penny stocks if desired
                penny_stocks.append({"symbol": symbol, "name": name})
                logging.info(f"Added penny stock: {symbol} at ${price}")
        except Exception as e:
            logging.warning(f"Skipping {symbol}: {e}")
            continue
    
    # Save watchlist.json
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(penny_stocks, f, indent=2)
    
    logging.info(f"Watchlist saved with {len(penny_stocks)} penny stocks")
except Exception as e:
    logging.error(f"❌ Failed to fetch tickers: {e}")
    penny_stocks = []

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
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")  # get last 2 days for percent change
        if len(data) < 2:
            continue
        
        latest_close = data['Close'][-1]
        prev_close = data['Close'][-2]
        percent_change = round((latest_close - prev_close) / prev_close * 100, 2) if prev_close else 0
        
        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": round(latest_close, 2),
            "percent_change": percent_change
        })
        
        logging.info(f"{symbol} → ${latest_close} ({percent_change}%)")
    except Exception as e:
        logging.error(f"❌ Error collecting data for {symbol}: {e}")
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

logging.info("Daily stock data saved")
logging.info("🎉 Collector completed successfully")
print(f"Daily stock data updated at {daily_entry['timestamp']}")
