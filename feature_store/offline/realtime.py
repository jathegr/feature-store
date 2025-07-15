import pandas as pd
from datetime import datetime, timedelta
from feature_store.offline.ingestion import fetch_eod_for_ticker
from feature_store.offline.transforms import build_features
from feature_store.offline.storage import write_features

def realtime_update(symbols: list[str]):
    """
    Fetch yesterday's EOD, compute features, and append.
    """
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    frames = []

    for sym in symbols:
        df_raw = fetch_eod_for_ticker(sym, start=yesterday, end=yesterday)
        if df_raw.empty: 
            continue
        df_raw = df_raw.assign(date=lambda x: x.date.str[:10], symbol=sym)
        df_feat = build_features(df_raw)
        frames.append(df_feat)

    if frames:
        df_all = pd.concat(frames, ignore_index=True)
        write_features(df_all, "engineered", partition_cols=["symbol", "date"])
        print(f"Real-time update: {len(frames)} symbols processed.")