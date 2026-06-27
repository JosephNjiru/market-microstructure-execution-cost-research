from __future__ import annotations

import pandas as pd


def accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float((y_true == y_pred).mean())
