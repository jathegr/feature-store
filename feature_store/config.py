# feature_store/config.py

from pathlib import Path
import os

# -----------------------------------------------------------------------------
# Base directories
# -----------------------------------------------------------------------------
BASE_DIR     = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FEATURE_DIR  = BASE_DIR / "data" / "features"

# -----------------------------------------------------------------------------
# Marketstack ingestion settings
# -----------------------------------------------------------------------------
API_KEYS    = [
    "49969228e60cd199c833af883f71daf8",
    "a1b6b988d3e963d2acc35c26c4f6937c",
    "1c8daeb3c47ed78b4c13ae07b5f382ec",
    "517447fdea36c5a1314711ffc56001ce",
    "9ea5391f9d2ee0ee342f3c6504e5b099",
    "45ccbd650ee61dacbf0ddebbd9019af8",
    "a4eb6b98c9706fd0eda8351a30bdc722"
]
FETCH_LIMIT = 1000           # Number of records per API request
START_DATE  = "2018-01-01"   # Earliest date to fetch (YYYY-MM-DD)
END_DATE    = None           # None = up to today

# -----------------------------------------------------------------------------
# SQL database (SQLite or Postgres) integration
# -----------------------------------------------------------------------------
# Example:
#   SQLite:     sqlite:///feature_store.db
#   Postgres:   postgresql+psycopg2://user:pass@host:5432/dbname
DB_URL = os.getenv("DB_URL", "sqlite:///feature_store.db")

# -----------------------------------------------------------------------------
# Redis cache (optional)
# -----------------------------------------------------------------------------
# Format: redis://[:password@]host:port/db
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# -----------------------------------------------------------------------------
# iCloud Drive cache directory (Windows)
# -----------------------------------------------------------------------------
# Syncs pickled objects via your Windows iCloudDrive
ICLOUD_CACHE_DIR = Path("C:/Users/user/iCloudDrive/feature_store_cache")
ICLOUD_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# S3 cache (optional, if you have access)
# -----------------------------------------------------------------------------
S3_BUCKET  = os.getenv("S3_BUCKET", "my-feature-store-cache")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# -----------------------------------------------------------------------------
# Backfill & real-time settings
# -----------------------------------------------------------------------------
BACKFILL_BATCH_SIZE   = int(os.getenv("BACKFILL_BATCH_SIZE", 500))
REALTIME_WINDOW_DAYS  = int(os.getenv("REALTIME_WINDOW_DAYS", 1))