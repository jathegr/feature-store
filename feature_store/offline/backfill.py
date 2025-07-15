import pandas as pd
from datetime import timedelta
from feature_store.offline.storage import read_features, write_features
from feature_store.offline.transforms import build_features

def backfill_feature_range(
    feature_name: str,
    symbols: list[str],
    full_start: str,
    full_end: str
):
    """
    Detect missing dates per symbol and fill them by recomputing features.
    """
    df = read_features(feature_name, symbols=symbols, start=full_start, end=full_end)
    all_dates = pd.date_range(full_start, full_end, freq="D")
    out_frames = []

    for sym in symbols:
        sub = df[df.symbol == sym].set_index("date").reindex(all_dates)
        sub["symbol"] = sym
        sub = sub.reset_index().rename(columns={"index": "date"})
        # re-compute transforms for NaN rows
        sub = build_features(sub)
        out_frames.append(sub)

    result = pd.concat(out_frames, ignore_index=True)
    write_features(result, feature_name, partition_cols=["symbol", "date"])
    print(f"Backfilled {feature_name} for {len(symbols)} symbols.")