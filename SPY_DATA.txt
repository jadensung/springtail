import yfinance as yf
import datetime
import os
import json
import pandas as pd  


date1 = datetime.datetime.today()
date2 = date1 - datetime.timedelta(days=30)


spy_data = yf.download('SPY', start=date2, end=date1, interval='1d')


columns = ['Close', 'High', 'Low', 'Open', 'Volume']
selected_data = spy_data[columns].round(6)


if isinstance(selected_data.columns, pd.MultiIndex):
    selected_data.columns = selected_data.columns.get_level_values(0)


data_json = {"ticker": "SPY", "data": []}


for date in selected_data.index:
    row = selected_data.loc[date]
    data_json["data"].append({
        "Date": date.strftime('%Y-%m-%d'),
        "Close": float(row["Close"]),
        "High": float(row["High"]),
        "Low": float(row["Low"]),
        "Open": float(row["Open"]),
        "Volume": int(row["Volume"])
    })


folder_path = r"C:\Users\Jaden\Desktop\spy_data"
os.makedirs(folder_path, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"spy_data_clean_{timestamp}.json"
json_path = os.path.join(folder_path, filename)


with open(json_path, 'w') as f:
    json.dump(data_json, f, indent=4)

print(f"Saved clean JSON to {json_path}")