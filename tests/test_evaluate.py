# tests/test_evaluate.py

import numpy as np
import pandas as pd
import pytest

from predictive_model.src.evaluate import (
    evaluate_classification,
    backtest_strategy
)

def test_evaluate_classification_perfect_auc():
    """
    With perfectly separable probabilities,
    ROC AUC should equal 1.0.
    """
    y = np.array([0, 1, 0, 1])
    proba = np.array([0.1, 0.9, 0.2, 0.8])
    metrics = evaluate_classification(y, proba, threshold=0.5)
    assert metrics['roc_auc'] == pytest.approx(1.0)


def test_backtest_strategy_returns_cumprod():
    """
    If we always go long (proba=1), cumulative return
    should match (110/100)*(120/110) = 1.2.
    """
    feat_df = pd.DataFrame({
        'symbol': ['Z', 'Z', 'Z'],
        'date': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']),
        'close': [100, 110, 120]
    })
    # All probabilities = 1 → always long
    daily, performance = backtest_strategy(feat_df, np.ones(3), threshold=0.5)

    # Extract the lone final_return scalar
    final_return = performance['final_return'].iloc[0]
    assert final_return == pytest.approx(1.2)
