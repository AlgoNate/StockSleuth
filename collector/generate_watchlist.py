import json
from datetime import datetime

# Example: replace this with your real stock collector output
watchlist_data = [
    {
        "symbol": "ABC",
        "name": "ABC Corp",
        "price": 1.23,
        "percent_change": 2.34,
        "price_history": [1.15, 1.18, 1.20, 1.22, 1.23]
    },
    {
        "symbol": "XYZ",
        "name": "XYZ Inc",
        "price": 0.87,
        "percent_change": -1.56,
        "price_history": [0.90, 0.88, 0.89, 0.87, 0.87]
    }
]

# Add local timestamp
local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
watchlist_with_timestamp = {
    "last_updated": local_time,
    "stocks": watchlist_data
}

# Save JSON
with open("collector/watchlist.json", "w") as f:
    json.dump(watchlist_with_timestamp, f, indent=2)
