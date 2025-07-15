#!/usr/bin/env python3
"""
preprocess.py

Cleans and aligns raw OHLCV data:
- Parses dates and numeric types
- Drops duplicates and sorts
- Forward/back-fills missing values
- Caps outliers based on median price
"""

import pandas as pd

def preprocess_raw(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and align raw OHLCV data:
    - Parse dates
    - Sort by symbol & date
    - Drop duplicates
    - Forward-/back-fill missing values
    - Remove extreme outliers
    """
    # 1. Parse dates and numeric columns
    df["date"]   = pd.to_datetime(df["date"]).dt.date
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 2. Deduplicate and sort
    df = df.drop_duplicates(subset=["symbol", "date"])
    df = df.sort_values(["symbol", "date"])

    # 3. Fill gaps in price and volume
    price_cols = ["open", "high", "low", "close"]
    df[price_cols] = (
        df.groupby("symbol")[price_cols]
          .ffill()
          .bfill()
    )
    df["volume"] = (
        df.groupby("symbol")["volume"]
          .ffill()
          .fillna(0)
    )

    # 4. Cap outliers in close price
    def cap_outliers(x: pd.Series) -> pd.Series:
        med = x.median()
        lower, upper = med * 0.2, med * 5
        return x.clip(lower=lower, upper=upper)

    df["close"] = df.groupby("symbol")["close"].transform(cap_outliers)

    return df.reset_index(drop=True)