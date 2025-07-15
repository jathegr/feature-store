import requests
import pandas as pd
from datetime import datetime
from itertools import cycle
from typing import List, Optional
from feature_store.config import API_KEYS, FETCH_LIMIT, START_DATE, END_DATE

BASE_URL = "https://api.marketstack.com/v1/eod"

def fetch_eod_for_ticker(
    ticker: str,
    start: str = START_DATE,
    end: Optional[str] = END_DATE
) -> pd.DataFrame:
    """
    Fetch end-of-day OHLCV for a single ticker.
    """
    params = {
        "access_key": None,
        "symbols": ticker,
        "limit": FETCH_LIMIT,
        "date_from": start
    }
    if end:
        params["date_to"] = end

    # Rotate keys
    for key in cycle(API_KEYS):
        params["access_key"] = key
        res = requests.get(BASE_URL, params=params)
        if res.status_code == 200:
            data = res.json().get("data", [])
            return pd.DataFrame(data)
        elif res.status_code == 429:
            continue  # key exhausted, try next
        else:
            res.raise_for_status()
    raise RuntimeError("All API keys exhausted or failed.")

def fetch_bulk_eod(
    tickers: List[str],
    start: str = START_DATE,
    end: Optional[str] = END_DATE
) -> pd.DataFrame:
    """
    Fetch EOD data for multiple tickers and concatenate.
    """
    frames = []
    for ticker in tickers:
        df = fetch_eod_for_ticker(ticker, start, end)
        if not df.empty:
            df["symbol"] = ticker
            frames.append(df)
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()