# tests/test_data_loader.py

import pandas as pd
import pytest

from predictive_model.src.data_loader import load_dataset

class DummyClient:
    def __init__(self, url):
        # no-op stub constructor
        pass

    def get_features(self, symbols, start=None, end=None):
        # return a minimal DataFrame for testing
        return pd.DataFrame({
            'symbol': ['A', 'A'],
            'date': pd.to_datetime(['2021-01-01', '2021-01-02']),
            'close': [100, 110]
        })

@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    """
    Monkey-patch the real FeatureStoreClient to use DummyClient
    so tests run offline without hitting a real feature store.
    """
    monkeypatch.setattr(
        'predictive_model.src.data_loader.FeatureStoreClient',
        DummyClient
    )

def test_load_dataset_shapes():
    """
    load_dataset should:
    - drop the last row per symbol (since no future close to label)
    - return X, y of equal length
    - when return_full_df=False, not include 'label' column in X
    """
    X, y = load_dataset(
        symbols=['A'],
        start=None,
        end=None,
        fs_url='dummy',          # passed to our DummyClient
        return_full_df=False
    )

    # We had two rows per symbol; after dropping last, only one sample remains
    assert X.shape[0] == 1
    assert y.shape[0] == 1

    # X should not contain the label column when return_full_df=False
    assert 'label' not in X.columns
