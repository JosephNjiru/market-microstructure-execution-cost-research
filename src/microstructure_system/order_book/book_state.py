from __future__ import annotations

import pandas as pd


def best_bid(snapshot: pd.Series) -> float:
    return float(snapshot["bid_price_1"])


def best_ask(snapshot: pd.Series) -> float:
    return float(snapshot["ask_price_1"])


def mid_price(snapshot: pd.Series) -> float:
    return (best_bid(snapshot) + best_ask(snapshot)) / 2
