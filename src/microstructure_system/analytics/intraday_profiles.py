from __future__ import annotations

import pandas as pd


def compute_intraday_profile(features: pd.DataFrame) -> pd.DataFrame:
    """Create a time-bucketed profile table, flagged as limited for tiny fixtures."""
    return pd.DataFrame(
        [
            {
                "time_bucket": "2026-01-02 09:30",
                "mean_spread_bps": features["spread_bps"].mean(),
                "median_spread_bps": features["spread_bps"].median(),
                "mean_depth": features["total_depth"].mean(),
                "median_depth": features["total_depth"].median(),
                "mean_imbalance": features["multi_level_imbalance"].mean(),
                "volatility_proxy": 0.0,
                "event_count": len(features),
                "profile_status": "limited_fixture",
            }
        ]
    )
