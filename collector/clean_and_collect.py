#!/usr/bin/env python3
# File: collector/clean_and_collect.py

import os
import json
from datetime import datetime
import yfinance as yf

SCHEMA_FILE = "collector/daily_stock_data.schema.json"
DATA_FILE = "collector/daily_stock_data.json"
WATCHLIST_FILE = "collector/watchlist.json"

symbols_to_check = [
    "GME","AMC","PLUG","NOK","SNDL","VKSC","UCLE",
    "PPCB","BIEL","CYAN","GLNLF","CPMD","DMIFF",
    "NRXPW","IDGC","VHAI","ARRRF","BFYW","ANORF","AMHGQ"
]

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load {path}: {e}")
    return None

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def clean_old_data(data):
    """Keep only entries where every stock has required fields."""
    cleaned = []
    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            continue
        timestamp = entry.get("timestamp")
        stocks = entry.get("stocks")
        if not isinstance(stocks, list):
            continue
        valid_stocks = []
        for s in stocks:
            # check required keys
            if all (k in s for k in ("symbol","name","price","percent_change")):
                valid_stocks.append(s)
            else:
                print(f"Removed invalid stock in entry {idx}: {s}")
        # Only keep entries where stocks is a non-empty list
        if valid_stocks:
            cleaned.append({
                "timestamp": timestamp,
                "stocks": valid_stocks
            })
        else:
            print(f"Removed entire entry {idx} (no valid stocks left)")
    return cleaned

def collect_penny_stocks():
    results = []
    for symbol in symbols_to_check:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", auto_adjust=False)
            if hist.empty or "Close" not in hist.columns:
                continue
            price = float(hist["Close"].iloc[-1])
            prev_close = float(hist["Close"].iloc[-2]) if hist.shape[0] >= 2 else price
            if not (0 < price <= 1):
                continue
            name = ticker.info.get("shortName", symbol)
            percent_change = round((price - prev_close)/prev_close * 100, 2) if prev_close else 0.0
            results.append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "percent_change": percent_change
            })
        except Exception as e:
            print(f"⚠️ Error fetching {symbol}: {e}")
            continue
    return results

def main():
    # 1. Clean old data
    old = load_json(DATA_FILE)
    if old is None:
        old = []
    cleaned = clean_old_data(old)

    # 2. Save cleaned history
    save_json(cleaned, DATA_FILE)
    print(f"✅ Cleaned old data; now {len(cleaned)} valid entries remain.")

    # 3. Run fresh collection
    penny = collect_penny_stocks()
    if penny:
        new_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "stocks": penny
        }
        cleaned.append(new_entry)
        save_json(cleaned, DATA_FILE)
        print(f"✅ Added new entry with {len(penny)} stocks. Total entries: {len(cleaned)}")
    else:
        print("⚠️ No penny stocks found in this run; no new entry added.")

    # 4. Update watchlist
    with open(WATCHLIST_FILE, "w") as f:
        json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in penny], f, indent=2)
    print("✅ Watchlist updated.")

if __name__ == "__main__":
    main()
