import requests
from typing import Dict

API_URL = "http://localhost:8000/features"

def fetch_feature_vector(symbol: str, date: str) -> Dict:
    res = requests.post(API_URL, json={"symbol": symbol, "date": date})
    res.raise_for_status()
    return res.json()

# feature_store/online/client.py

"""
Stub implementation of feature_store.online.client.FeatureStoreClient
for local testing and import resolution.
"""

class FeatureStoreClient:
    def __init__(self, url: str):
        """
        Initialize the client stub. 
        In production this would set up a connection to your feature store,
        but here it's a no-op so tests can import it without errors.
        """
        self.url = url

    def get_features(self, symbols, start=None, end=None):
        """
        Stub method signature for fetching feature data.
        Tests should monkey-patch or subclass this
        to return dummy DataFrames.
        """
        raise NotImplementedError(
            "FeatureStoreClient.get_features is a stub. "
            "Override in tests to return dummy data."
        )
