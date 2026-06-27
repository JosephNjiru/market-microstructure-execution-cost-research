from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.visualisation.common import write_bar_figure


def write_stage2_figures(
    project_root: Path,
    features: pd.DataFrame,
    labels: pd.DataFrame,
    model_performance: pd.DataFrame,
) -> None:
    """Write Stage 2 diagnostic figures."""
    figures = [
        ("order_book_spread_through_time.png", features["spread_bps"], "Order book spread through time"),
        ("depth_imbalance_distribution.png", features["depth_imbalance"], "Depth imbalance distribution"),
        ("microprice_vs_midprice.png", features["microprice_minus_mid"], "Microprice versus mid-price"),
        ("liquidity_regime_counts.png", features["liquidity_regime"].value_counts(), "Liquidity regime counts"),
        ("short_horizon_label_distribution.png", labels["movement_label_1_event"].value_counts(), "Short-horizon label distribution"),
        ("event_intensity_profile.png", pd.Series([1.0]), "Event intensity profile"),
        ("baseline_model_performance.png", model_performance["accuracy"], "Baseline model performance"),
    ]
    for filename, series, title in figures:
        write_bar_figure(project_root / "reports/figures" / filename, series, title)
