#!/usr/bin/env python3
# File: collector/clean_and_collect.py

import os
import json
from datetime import datetime
import yfinance as yf

DATA_FILE = "collector/daily_stock_data.json"
WATCHLIST_FILE = "collector/watchlist.json"

symbols_to_check = [
    "GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"
]

def fetch_penny_stocks(symbols):
    output = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", auto_adjust=False)
            if hist.empty or "Close" not in hist.columns:
                print(f"⚠️ Skipping {symbol}: no close price data")
                continue

            price = float(hist["Close"].iloc[-1])
            if price <= 0 or price > 1:
                # not a penny stock by your criterion
                continue

            prev_close = float(hist["Close"].iloc[-2]) if hist.shape[0] >= 2 else price
            if prev_close == 0:
                percent_change = 0.0
            else:
                percent_change = round((price - prev_close) / prev_close * 100, 2)

            stock = {
                "symbol": symbol,
                "name": ticker.info.get("shortName", symbol),
                "price": price,
                "percent_change": percent_change
            }
            output.append(stock)
        except Exception as e:
            print(f"⚠️ Error fetching {symbol}: {e}")
            continue
    return output

def clean_history(data):
    cleaned = []
    for entry in data:
        stocks = entry.get("stocks", [])
        valid = []
        for s in stocks:
            if all(k in s for k in ("symbol","name","price","percent_change")):
                valid.append(s)
            else:
                print("Removed stock missing required fields:", s)
        if valid:
            cleaned.append({"timestamp": entry.get("timestamp"), "stocks": valid})
    return cleaned

def read_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    # 1. Clean existing history
    old = read_json(DATA_FILE)
    cleaned = clean_history(old)
    print(f"Cleaned history — kept {len(cleaned)} valid entries.")

    # 2. Fetch new data
    new_stocks = fetch_penny_stocks(symbols_to_check)
    print(f"Fetched {len(new_stocks)} valid penny stocks.")

    if not new_stocks:
        print("No valid stocks found — not appending new entry.")
    else:
        new_entry = {"timestamp": datetime.utcnow().isoformat(), "stocks": new_stocks}
        cleaned.append(new_entry)
        write_json(DATA_FILE, cleaned)
        print("Appended new entry. Total entries now:", len(cleaned))

        # Update watchlist
        with open(WATCHLIST_FILE, "w") as f:
            json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in new_stocks], f, indent=2)
        print("Watchlist updated.")

if __name__ == "__main__":
    main()
