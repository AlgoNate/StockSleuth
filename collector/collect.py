import os
import json
import yfinance as yf
from datetime import datetime

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"
LOG_FILE = "collector/collector.log"

# Ensure files/folders exist
os.makedirs(HISTORY_DIR, exist_ok=True)
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE, "w") as f:
        json.dump([], f)

# Optional: clear log each run
with open(LOG_FILE, "w") as log:
    log.write(f"Run started: {datetime.utcnow().isoformat()}\n")

# Example watchlist symbols (replace or extend as needed)
symbols_to_check = [
    "GME", "AMC", "PLUG", "NOK", "SNDL", "VKSC", "UCLE", "PPCB",
    "BIEL", "CYAN", "GLNLF", "CPMD", "DMIFF", "NRXPW", "IDGC",
    "VHAI", "ARRRF", "BFYW", "ANORF", "AMHGQ"
]

penny_stocks = []

# Scan symbols for penny stocks (price <= $1)
for symbol in symbols_to_check:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                penny_stocks.append({"symbol": symbol, "name": name, "price": price})
                with open(LOG_FILE, "a") as log:
                    log.write(f"✅ {symbol} added: ${price}\n")
    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"⚠️ Could not fetch {symbol}: {e}\n")

# Save watchlist.json
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)

# Create daily entry
daily_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "stocks": penny_stocks
}

# Append to daily_stock_data.json
with open(DAILY_DATA_FILE, "r") as f:
    data = json.load(f)
data.append(daily_entry)
with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Save a copy in history folder with date
history_file = os.path.join(HISTORY_DIR, f"{datetime.utcnow().strftime('%Y-%m-%d')}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

# Log completion
with open(LOG_FILE, "a") as log:
    log.write(f"✅ Daily stock data updated with {len(penny_stocks)} penny stocks\n")
