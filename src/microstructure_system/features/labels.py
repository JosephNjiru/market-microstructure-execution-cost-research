from __future__ import annotations

import numpy as np
import pandas as pd


def add_short_horizon_labels(features: pd.DataFrame) -> pd.DataFrame:
    """Create future mid-price movement labels for diagnostic modelling only."""
    labels = features[["timestamp_utc", "mid_price", "source", "source_dataset"]].copy()
    for horizon in [1, 3, 5, 10]:
        future = features["mid_price"].shift(-horizon)
        returns = (future - features["mid_price"]) / features["mid_price"]
        labels[f"future_mid_price_{horizon}_event"] = future
        labels[f"mid_price_change_{horizon}_event"] = future - features["mid_price"]
        labels[f"mid_price_return_{horizon}_event"] = returns
        labels[f"movement_label_{horizon}_event"] = np.where(
            returns > 0,
            "up",
            np.where(returns < 0, "down", "flat"),
        )
        labels.loc[future.isna(), f"movement_label_{horizon}_event"] = "insufficient_future"
        labels[f"label_boundary_flag_{horizon}_event"] = future.isna()
    return labels


def summarise_label_distribution(labels: pd.DataFrame) -> pd.DataFrame:
    """Summarise short-horizon movement label counts by horizon."""
    rows = []
    for horizon in [1, 3, 5, 10]:
        counts = labels[f"movement_label_{horizon}_event"].value_counts()
        for label, count in counts.items():
            rows.append(
                {
                    "horizon": f"{horizon}_event",
                    "movement_label": label,
                    "row_count": int(count),
                    "claim_boundary": "Predictive diagnostic only. No execution-cost claim.",
                }
            )
    return pd.DataFrame(rows)
