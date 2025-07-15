#!/usr/bin/env python3
"""
Orchestrates ingestion, preprocessing, transformation, and storage of features,
with iCloud caching of raw EOD data.
"""

import pickle
from pathlib import Path

from feature_store.config import ICLOUD_CACHE_DIR
from feature_store.utils.cache_icloud import ICloudCache
from feature_store.offline.ingestion import fetch_bulk_eod
from feature_store.offline.preprocess import preprocess_raw
from feature_store.offline.transforms import build_features
from feature_store.offline.storage import write_features

def main():
    # 1. Load tickers
    tickers_path = Path("stock_tickers.txt")
    if tickers_path.exists():
        tickers = tickers_path.read_text().splitlines()
    else:
        tickers = ["AAPL", "MSFT", "TSLA"]

    # 2. Cache or fetch raw EOD data
    cache = ICloudCache("raw_eod_data")
    raw_df = cache.get()
    if raw_df is None:
        raw_df = fetch_bulk_eod(tickers)
        if raw_df.empty:
            print("No raw data fetched.")
            return
        cache.set(raw_df)

    # 3. Standardize and sort dates
    raw_df["date"] = raw_df["date"].str[:10]
    raw_df = raw_df.sort_values(["symbol", "date"])

    # 4. Preprocess: parse types, fill gaps, cap outliers
    raw_df = preprocess_raw(raw_df)

    # 5. Compute technical features
    feat_df = build_features(raw_df)

    # 6. Persist engineered features
    write_features(
        df=feat_df,
        feature_name="engineered",
        partition_cols=["symbol", "date"]
    )
    print("Feature store build complete.")

if __name__ == "__main__":
    main()