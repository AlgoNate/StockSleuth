import os
import json
import yfinance as yf
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

WATCHLIST_FILE = "collector/watchlist.json"
DAILY_DATA_FILE = "collector/daily_stock_data.json"
HISTORY_DIR = "collector/history"
LOG_FILE = "collector/collector.log"

os.makedirs(HISTORY_DIR, exist_ok=True)

symbols_to_check = [
    "GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"
]

def log(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {message}\n")

def check_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            price = float(data["Close"].iloc[-1])
            if 0 < price <= 1:
                name = ticker.info.get("shortName", symbol)
                log(f"✅ {symbol} added: ${price}")
                return {"symbol": symbol, "name": name, "price": price}
    except Exception as e:
        log(f"⚠️ Could not fetch {symbol}: {e}")
    return None

# Parallel execution
log("🔎 Scanning symbols for penny stocks (price <= $1)...")
penny_stocks = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_stock, s) for s in symbols_to_check]
    for future in as_completed(futures):
        result = future.result()
        if result:
            penny_stocks.append(result)

# Save watchlist
with open(WATCHLIST_FILE, "w") as f:
    json.dump(penny_stocks, f, indent=2)
log(f"✅ Watchlist saved with {len(penny_stocks)} penny stocks.")

# Save daily data
daily_entry = {"timestamp": datetime.utcnow().isoformat(), "stocks": penny_stocks}

data = []
if os.path.exists(DAILY_DATA_FILE):
    with open(DAILY_DATA_FILE) as f:
        data = json.load(f)
data.append(daily_entry)

with open(DAILY_DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# Save history with timestamp
history_file = os.path.join(HISTORY_DIR, f"daily_stock_data_{datetime.utcnow().strftime('%Y%m%d')}.json")
with open(history_file, "w") as f:
    json.dump(daily_entry, f, indent=2)

log(f"✅ Daily stock data updated at {daily_entry['timestamp']}")
log(f"📂 History saved: {history_file}")
