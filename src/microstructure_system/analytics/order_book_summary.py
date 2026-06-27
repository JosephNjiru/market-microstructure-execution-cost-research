from __future__ import annotations

import pandas as pd


def summarise_order_book_features(features: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics for core order book feature columns."""
    columns = [
        "mid_price",
        "quoted_spread",
        "spread_bps",
        "total_depth",
        "top_level_imbalance",
        "multi_level_imbalance",
        "microprice_minus_mid",
    ]
    return pd.DataFrame(
        [
            {
                "feature_name": column,
                "mean": features[column].mean(),
                "median": features[column].median(),
                "minimum": features[column].min(),
                "maximum": features[column].max(),
            }
            for column in columns
        ]
    )
