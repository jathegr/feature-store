#!/usr/bin/env python3
"""
Batch backfill feature store for missing dates,
tracking progress via iCloud caching.
"""

from pathlib import Path

from feature_store.config import BACKFILL_BATCH_SIZE, START_DATE
from feature_store.offline.backfill import backfill_feature_range
from feature_store.utils.cache_icloud import ICloudCache

def main():
    # Load symbols
    tickers_path = Path("stock_tickers.txt")
    symbols = tickers_path.read_text().splitlines() if tickers_path.exists() else []

    # Resume from last batch index
    cache = ICloudCache("backfill_cursor")
    cursor = cache.get() or 0

    # Partition into batches
    batches = [
        symbols[i : i + BACKFILL_BATCH_SIZE]
        for i in range(0, len(symbols), BACKFILL_BATCH_SIZE)
    ]

    # Process batches from cursor onwards
    for idx in range(cursor, len(batches)):
        batch = batches[idx]
        backfill_feature_range("engineered", batch, START_DATE, None)
        cache.set(idx + 1)

    print("Backfill complete.")

if __name__ == "__main__":
    main()