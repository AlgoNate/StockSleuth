import json

# Generate 25 sample penny stocks
data = [{"symbol": f"PENNY{i}", "price": round(0.5 + i*0.01, 3), "percent_change": 10+i} for i in range(25)]

# Save to JSON
with open("collector/daily_stock_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Daily data collected")
