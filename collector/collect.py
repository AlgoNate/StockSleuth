import os
import json
from datetime import datetime
import yfinance as yf

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"

# Ensure necessary files and directories exist
os.makedirs(HISTORY_DIR, exist_ok=True)
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "w") as f:
        json.dump([], f)

# Example symbols; extend this list as needed
symbols_to_check = [
    "GME", "AMC", "PLUG", "NOK", "SNDL", "VKSC", "UCLE", "PPCB",
    "BIEL", "CYAN", "GLNLF", "CPMD", "DMIFF", "NRXPW", "IDGC",
    "VHAI", "ARRRF", "BFYW", "ANORF", "AMHGQ"
]

penny_stocks = []

print("🔎 Scanning symbols for penny stocks (price <= $1)...")

for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({"symbol": symbol, "name": name, "price": price})
                print(f"✅ {symbol} added: ${price}")
    except Exception as e:
        print(f"⚠️ Could not fetch {symbol}: {e}")

# Save watchlist.json
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

print(f"✅ Watchlist generated with {len(penny_stocks)} penny stocks.")

# Collect daily stock data
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": []
}

for stock in penny_stocks:
    symbol = stock["symbol"]
    name = stock["name"]
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        price = float(data["Close"].iloc[-1])
        prev_close = float(data["Close"].iloc[-2]) if len(data) > 1 else price
        percent_change = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0

        daily_entry["stocks"].append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "percent_change": percent_change
        })
    except Exception as e:
        print(f"⚠️ Could not fetch daily data for {symbol}: {e}")

# Append to daily_stock_data.json
with open(DAILY_DATA_FILE, "r") as f:
    all_data = json.load(f)

all_data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(all_data, f, indent=2)

# Save individual entry to history for easy debugging
history_file = os.path.join(HISTORY_DIR, f"{daily_entry['timestamp'].replace(':','-')}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

print(f"✅ Daily stock data saved with {len(daily_entry['stocks'])} stocks at {daily_entry['timestamp']}")
