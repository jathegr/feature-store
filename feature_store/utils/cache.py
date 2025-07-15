#legacy cache system

import os
import pickle
from pathlib import Path
from typing import Any

CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

class DiskCache:
    def __init__(self, namespace: str):
        self.path = CACHE_DIR / f"{namespace}.pkl"

    def get(self) -> Any:
        if self.path.exists():
            with open(self.path, "rb") as f:
                return pickle.load(f)
        return None

    def set(self, obj: Any) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(obj, f)