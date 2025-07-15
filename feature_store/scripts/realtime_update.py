#!/usr/bin/env python3
"""
Scheduled job for real-time feature updates,
using iCloud cache to store symbol list.
"""

from pathlib import Path

from feature_store.config import REALTIME_WINDOW_DAYS
from feature_store.offline.realtime import realtime_update
from feature_store.utils.cache_icloud import ICloudCache

def main():
    # Load or cache the symbol list
    tickers_path = Path("stock_tickers.txt")
    symbols = tickers_path.read_text().splitlines() if tickers_path.exists() else []

    cache = ICloudCache("realtime_symbols")
    cached = cache.get()
    if cached is None:
        cache.set(symbols)
    else:
        symbols = cached

    # Perform the update
    realtime_update(symbols)

if __name__ == "__main__":
    main()