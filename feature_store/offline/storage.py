import pandas as pd
from pathlib import Path
from typing import Optional
from feature_store.config import FEATURE_DIR

def write_features(
    df: pd.DataFrame,
    feature_name: str,
    partition_cols: Optional[list[str]] = None
) -> None:
    """
    Persist features as Parquet, partitioned by date and/or symbol.
    """
    path = FEATURE_DIR / feature_name
    path.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        path,
        partition_cols=partition_cols or ["symbol", "date"],
        engine="pyarrow",
        index=False
    )

def read_features(
    feature_name: str,
    symbols: Optional[list[str]] = None,
    start: Optional[str] = None,
    end:   Optional[str] = None
) -> pd.DataFrame:
    """
    Read back features, with optional filtering.
    """
    path = FEATURE_DIR / feature_name
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_parquet(path, engine="pyarrow")
    if symbols:
        df = df[df["symbol"].isin(symbols)]
    if start:
        df = df[df["date"] >= start]
    if end:
        df = df[df["date"] <= end]
    return df.reset_index(drop=True)