from __future__ import annotations

import pandas as pd


def top_level_imbalance(best_bid_size: float, best_ask_size: float) -> float | None:
    denominator = best_bid_size + best_ask_size
    return None if denominator == 0 else (best_bid_size - best_ask_size) / denominator


def summarise_imbalance(features: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "imbalance_measure": ["top_level_imbalance", "multi_level_imbalance"],
            "mean": [features["top_level_imbalance"].mean(), features["multi_level_imbalance"].mean()],
            "zero_depth_flag_count": 0,
        }
    )
