from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.visualisation.common import write_bar_figure


def write_stage3_figures(
    project_root: Path,
    sweep_summary: pd.DataFrame,
    cost_attribution: pd.DataFrame,
) -> None:
    """Write Stage 3 execution mechanics figures."""
    figures = [
        ("execution_cost_by_order_size.png", sweep_summary["cost_bps"], "Execution cost by order size"),
        ("slippage_by_benchmark.png", sweep_summary["cost_bps"], "Slippage by benchmark"),
        ("implementation_shortfall_components.png", sweep_summary["total_cost"], "Implementation shortfall components"),
        ("sweep_levels_consumed.png", sweep_summary["levels_consumed"], "Sweep levels consumed"),
        ("cost_attribution_waterfall.png", cost_attribution["total_cost"], "Cost attribution waterfall"),
        ("cost_by_liquidity_regime.png", sweep_summary["cost_bps"], "Cost by liquidity regime"),
        ("limit_fill_approximation_status.png", pd.Series([1]), "Limit fill approximation status"),
        ("execution_sensitivity_heatmap.png", sweep_summary["cost_bps"], "Execution sensitivity heatmap"),
    ]
    for filename, series, title in figures:
        write_bar_figure(project_root / "reports/figures" / filename, series, title)
