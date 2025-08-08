import yfinance as yf
import datetime
import os
import json
import pandas as pd  
from pathlib import Path

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


base_folder = Path(__file__).parent
output_folder = base_folder / "spyoutput"
output_folder.mkdir(parents=True, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"spy_data_clean_{timestamp}.json"
json_path = os.path.join(output_folder, filename)


with open(json_path, 'w') as f:
    json.dump(data_json, f, indent=4)

print(f"Saved JSON to {json_path}")