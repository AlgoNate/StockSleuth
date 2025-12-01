import os
import json
import yfinance as yf
from datetime import datetime

# File paths
WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"

# Ensure watchlist file exists
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)

# Ensure history directory exists
os.makedirs(HISTORY_DIR, exist_ok=True)

# Symbols to check (extendable)
symbols_to_check = [
    "GME", "AMC", "PLUG", "NOK", "SNDL", "VKSC", "UCLE", "PPCB",
    "BIEL", "CYAN", "GLNLF", "CPMD", "DMIFF", "NRXPW", "IDGC",
    "VHAI", "ARRRF", "BFYW", "ANORF", "AMHGQ"
]

# Scan penny stocks
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

# Collect daily data entry
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": penny_stocks
}

# Append to daily_stock_data.json
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Save a copy in history with timestamp
history_filename = os.path.join(HISTORY_DIR, f"daily_stock_data_{datetime.utcnow().strftime('%Y%m%d')}.json")
with open(history_filename, "w") as f:
    json.dump(daily_entry, f, indent=2)

print(f"✅ Daily stock data updated at {daily_entry['timestamp']}")
print(f"📂 History saved: {history_filename}")
