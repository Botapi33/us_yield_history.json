import json
import os
from urllib.request import urlopen

API_KEY = os.environ.get("FRED_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing FRED_API_KEY")

URL = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key={API_KEY}&file_type=json&sort_order=asc"

data = json.loads(urlopen(URL).read().decode("utf-8"))

history = []

for o in data["observations"]:
    val = o["value"]
    if val not in (".", ""):
        history.append({
            "date": o["date"],
            "value": round(float(val), 4)
        })

# Begrenzen (Performance + sauberer Chart)
history = history[-500:]

with open("us_yield_history.json", "w") as f:
    json.dump(history, f, indent=2)

print("US history updated:", len(history))
