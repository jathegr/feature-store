import pandas as pd
from typing import List

def rolling_mean(df: pd.DataFrame, window: int) -> pd.Series:
    return df["close"].rolling(window).mean()

def rolling_std(df: pd.DataFrame, window: int) -> pd.Series:
    return df["close"].rolling(window).std()

def compute_bollinger(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = df.copy()
    df[f"bb_mean_{window}"] = rolling_mean(df, window)
    df[f"bb_std_{window}"]  = rolling_std(df, window)
    df[f"bb_upper_{window}"] = df[f"bb_mean_{window}"] + 2 * df[f"bb_std_{window}"]
    df[f"bb_lower_{window}"] = df[f"bb_mean_{window}"] - 2 * df[f"bb_std_{window}"]
    return df

def compute_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    delta = df["close"].diff()
    up, down = delta.clip(lower=0), -1 * delta.clip(upper=0)
    ma_up   = up.rolling(window).mean()
    ma_down = down.rolling(window).mean()
    rs = ma_up / ma_down
    df[f"rsi_{window}"] = 100 - (100 / (1 + rs))
    return df

def compute_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    exp1 = df["close"].ewm(span=fast, adjust=False).mean()
    exp2 = df["close"].ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    df["macd_line"]    = macd_line
    df["macd_signal"]  = signal_line
    df["macd_histogram"] = macd_line - signal_line
    return df

def build_features(df: pd.DataFrame, windows: List[int] = [5, 10, 20]) -> pd.DataFrame:
    df = compute_bollinger(df, windows[-1])
    df = compute_rsi(df, windows[1])
    df = compute_macd(df)
    return df