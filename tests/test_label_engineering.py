import pandas as pd
from predictive_model.src.label_engineering import make_labels

def test_make_labels_basic():
    df = pd.DataFrame({
        'symbol': ['X', 'X', 'Y', 'Y'],
        'date': pd.to_datetime([
            '2021-01-01', '2021-01-02',
            '2021-01-01', '2021-01-02'
        ]),
        'close': [100, 110, 200, 190]
    })
    labels = make_labels(df, threshold=0.0)
    # For X: 110/100=0.10>0 ⇒1; last row per symbol drops to 0
    assert labels.tolist() == [1, 0, 0, 0]
