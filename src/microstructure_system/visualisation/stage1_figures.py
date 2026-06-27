from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.visualisation.common import write_bar_figure


def write_stage1_figures(project_root: Path, book: pd.DataFrame, costs: pd.DataFrame) -> None:
    """Write Stage 1 fixture and sweep continuity figures."""
    spread = book["ask_price_1"] - book["bid_price_1"]
    figures = [
        ("tiny_lob_spread_example.png", spread, "Tiny LOB spread example"),
        ("tiny_lob_depth_example.png", book["bid_size_1"], "Tiny LOB depth example"),
        ("market_order_sweep_example.png", costs["total_cost"], "Market-order sweep example"),
        ("cost_attribution_example.png", costs["total_cost"], "Cost attribution example"),
    ]
    for filename, series, title in figures:
        write_bar_figure(project_root / "reports/figures" / filename, series, title)
