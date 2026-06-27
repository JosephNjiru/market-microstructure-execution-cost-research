from __future__ import annotations

import pandas as pd


def calculate_microprice(
    best_ask_price: float,
    best_bid_price: float,
    best_bid_size: float,
    best_ask_size: float,
) -> float | None:
    denominator = best_bid_size + best_ask_size
    if denominator == 0:
        return None
    return (best_ask_price * best_bid_size + best_bid_price * best_ask_size) / denominator


def summarise_microprice(features: pd.DataFrame) -> pd.DataFrame:
    """Summarise microprice displacement from the quoted mid-price."""
    return pd.DataFrame(
        [
            {
                "mean_microprice_minus_mid": features["microprice_minus_mid"].mean(),
                "signal_rows": int(features["microprice_signal_flag"].sum()),
            }
        ]
    )
