# Define feature data types/schema for validation or metadata
FEATURE_SCHEMA = {
    "symbol": "string",
    "date":   "date",
    "open":   "float",
    "high":   "float",
    "low":    "float",
    "close":  "float",
    "volume": "int",
    # engineered
    "bb_mean_20":     "float",
    "bb_std_20":      "float",
    "bb_upper_20":    "float",
    "bb_lower_20":    "float",
    "rsi_14":         "float",
    "macd_line":      "float",
    "macd_signal":    "float",
    "macd_histogram": "float",
}