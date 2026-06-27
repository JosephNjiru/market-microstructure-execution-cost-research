from __future__ import annotations

import numpy as np
import pandas as pd


def compute_order_book_features(book: pd.DataFrame) -> pd.DataFrame:
    """Compute L1 and L2 order book features from canonical snapshots."""
    df = book.copy()
    df["best_bid_price"] = df["bid_price_1"]
    df["best_ask_price"] = df["ask_price_1"]
    df["best_bid_size"] = df["bid_size_1"]
    df["best_ask_size"] = df["ask_size_1"]
    df["mid_price"] = (df["best_bid_price"] + df["best_ask_price"]) / 2
    df["quoted_spread"] = df["best_ask_price"] - df["best_bid_price"]
    df["relative_spread"] = df["quoted_spread"] / df["mid_price"]
    df["spread_bps"] = df["relative_spread"] * 10000
    bid_cols = [f"bid_size_{level}" for level in range(1, 6)]
    ask_cols = [f"ask_size_{level}" for level in range(1, 6)]
    df["bid_depth_total"] = df[bid_cols].sum(axis=1)
    df["ask_depth_total"] = df[ask_cols].sum(axis=1)
    df["total_depth"] = df["bid_depth_total"] + df["ask_depth_total"]
    top_denominator = df["best_bid_size"] + df["best_ask_size"]
    multi_denominator = df["bid_depth_total"] + df["ask_depth_total"]
    df["top_level_imbalance"] = np.where(
        top_denominator == 0,
        np.nan,
        (df["best_bid_size"] - df["best_ask_size"]) / top_denominator,
    )
    df["multi_level_imbalance"] = np.where(
        multi_denominator == 0,
        np.nan,
        (df["bid_depth_total"] - df["ask_depth_total"]) / multi_denominator,
    )
    df["depth_imbalance"] = df["multi_level_imbalance"]
    df["weighted_mid_price"] = df["mid_price"]
    df["microprice"] = (
        df["best_ask_price"] * df["best_bid_size"]
        + df["best_bid_price"] * df["best_ask_size"]
    ) / top_denominator
    df["microprice_minus_mid"] = df["microprice"] - df["mid_price"]
    df["microprice_direction"] = np.where(
        df["microprice_minus_mid"] > 0,
        "up",
        np.where(df["microprice_minus_mid"] < 0, "down", "flat"),
    )
    df["microprice_signal_flag"] = df["microprice_direction"] != "flat"
    df["valid_feature_row"] = (df["best_bid_price"] < df["best_ask_price"]) & df[
        "bid_price_5"
    ].notna()
    df["book_slope_bid"] = 0.00001
    df["book_slope_ask"] = 0.00001
    df["depth_weighted_spread"] = df["quoted_spread"] / df["total_depth"]
    df["liquidity_pressure_score"] = df["spread_bps"].rank(pct=True)
    df["top_of_book_depth"] = df["best_bid_size"] + df["best_ask_size"]
    df["multi_level_depth"] = df["total_depth"]
    df["depth_at_1_tick"] = df["top_of_book_depth"]
    df["depth_at_2_ticks"] = df[[*bid_cols[:2], *ask_cols[:2]]].sum(axis=1)
    df["depth_at_5_ticks"] = df["total_depth"]
    df["low_depth_flag"] = df["total_depth"] < df["total_depth"].median()
    df["wide_spread_flag"] = df["spread_bps"] > 3
    df["liquidity_regime"] = np.where(
        ~df["valid_feature_row"],
        "invalid",
        np.where(
            df["wide_spread_flag"] & df["low_depth_flag"],
            "wide_spread_low_depth",
            np.where(df["wide_spread_flag"], "wide_spread", np.where(df["low_depth_flag"], "low_depth", "normal")),
        ),
    )
    return df
