from __future__ import annotations

import pandas as pd


def summarise_liquidity_regimes(features: pd.DataFrame) -> pd.DataFrame:
    """Count rows assigned to each rule-based liquidity regime."""
    return features.groupby("liquidity_regime").size().reset_index(name="row_count")
