import requests
from typing import Dict

API_URL = "http://localhost:8000/features"

def fetch_feature_vector(symbol: str, date: str) -> Dict:
    res = requests.post(API_URL, json={"symbol": symbol, "date": date})
    res.raise_for_status()
    return res.json()