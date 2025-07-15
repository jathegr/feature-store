import pickle
import redis
from typing import Any
from feature_store.config import REDIS_URL

r = redis.from_url(REDIS_URL)

class RedisCache:
    def __init__(self, namespace: str):
        self.key = f"fs:{namespace}"

    def get(self) -> Any:
        data = r.get(self.key)
        return pickle.loads(data) if data else None

    def set(self, obj: Any) -> None:
        r.set(self.key, pickle.dumps(obj))