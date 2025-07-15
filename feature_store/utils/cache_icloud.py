#!/usr/bin/env python3
"""
cache_icloud.py

Stores pickled objects into your iCloud Drive folder for automatic sync.
"""

import pickle
from pathlib import Path
from feature_store.config import ICLOUD_CACHE_DIR

# Ensure the directory exists
ICLOUD_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class ICloudCache:
    def __init__(self, namespace: str):
        self.path = ICLOUD_CACHE_DIR / f"{namespace}.pkl"

    def get(self):
        if self.path.exists():
            with open(self.path, "rb") as f:
                return pickle.load(f)
        return None

    def set(self, obj):
        with open(self.path, "wb") as f:
            pickle.dump(obj, f)