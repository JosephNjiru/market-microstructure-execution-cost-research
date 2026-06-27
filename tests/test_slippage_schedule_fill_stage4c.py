from __future__ import annotations

import pandas as pd

from microstructure_system.execution.fill_model import approximate_limit_order_fills
from microstructure_system.execution.schedule import run_schedule_diagnostics
from microstructure_system.slippage.analysis import calculate_slippage_benchmarks
from microstructure_system.slippage.benchmarks import adverse_slippage


def test_slippage_benchmarks_include_vwap_and_twap(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, _, _ = sweep_outputs
    slippage = calculate_slippage_benchmarks(sweep)
    assert {"simple_vwap", "simple_twap"}.issubset(set(slippage["benchmark_type"]))


def test_adverse_slippage_is_side_aware() -> None:
    assert adverse_slippage("buy", 101, 100) == 1
    assert adverse_slippage("sell", 99, 100) == 1


def test_schedule_and_limit_fill_outputs_preserve_boundaries(
    execution_scenarios: pd.DataFrame,
) -> None:
    schedules = run_schedule_diagnostics(execution_scenarios)
    fills = approximate_limit_order_fills(execution_scenarios)
    assert {"vwap", "twap", "participation"} == set(schedules["schedule_type"])
    assert fills["requires_l3_for_exact_claim"].all()
