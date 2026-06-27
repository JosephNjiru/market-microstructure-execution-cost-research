from __future__ import annotations

import pandas as pd

from microstructure_system.execution.cost_attribution import (
    build_stage3_cost_attribution,
    components_reconcile,
)
from microstructure_system.execution.implementation_shortfall import (
    calculate_implementation_shortfall,
)
from microstructure_system.impact.market_impact import calculate_impact_proxies


def test_execution_scenarios_cover_schedules(execution_scenarios: pd.DataFrame) -> None:
    assert {"market_sweep", "vwap", "twap", "participation", "limit_order"}.issubset(
        set(execution_scenarios["schedule_type"])
    )


def test_market_sweep_records_fills_and_unfilled_residuals(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, fills, _ = sweep_outputs
    assert not fills.empty
    assert (sweep["unfilled_quantity"] > 0).any()


def test_cost_attribution_reconciles_after_impact_proxy(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, _, base_costs = sweep_outputs
    costs = build_stage3_cost_attribution(base_costs, calculate_impact_proxies(sweep))
    assert costs.apply(components_reconcile, axis=1).all()


def test_implementation_shortfall_is_non_negative(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, _, _ = sweep_outputs
    shortfall = calculate_implementation_shortfall(sweep)
    assert (shortfall["implementation_shortfall_bps"] >= 0).all()
