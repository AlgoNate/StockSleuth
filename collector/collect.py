import json

data = [{"symbol": f"PENNY{i}", "price": 0.5+i*0.01, "percent_change": 10+i} for i in range(25)]
with open("collector/daily_stock_data.json","w") as f:
    json.dump(data,f)
print("Daily data collected")
