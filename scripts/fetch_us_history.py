import json
import os
import urllib.request

API_KEY = os.environ.get("FRED_API_KEY")

if not API_KEY:
    raise Exception("Missing FRED_API_KEY")

url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key={API_KEY}&file_type=json&sort_order=asc"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

history = []

for o in data["observations"]:
    if o["value"] not in (".", ""):
        history.append({
            "date": o["date"],
            "value": float(o["value"])
        })

# Begrenzen (optional)
history = history[-2000:]

with open("us_yield_history.json", "w") as f:
    json.dump(history, f, indent=2)

print("US history updated:", len(history))
