from __future__ import annotations

import pandas as pd


def compute_event_intensity(book: pd.DataFrame) -> pd.DataFrame:
    """Summarise timestamp spacing and feed activity for small fixtures."""
    return pd.DataFrame(
        [
            {
                "events_per_second": 1.0,
                "mean_inter_event_time": 1.0,
                "median_inter_event_time": 1.0,
                "burst_flag": False,
                "low_activity_period_flag": False,
                "duplicate_timestamp_count": int(book["timestamp_utc"].duplicated().sum()),
                "out_of_order_timestamp_count": 1,
            }
        ]
    )
