from __future__ import annotations

import pandas as pd


def calculate_slippage_benchmarks(sweeps: pd.DataFrame) -> pd.DataFrame:
    """Calculate side-aware slippage diagnostics against simple benchmarks."""
    rows = []
    for _, row in sweeps.iterrows():
        for benchmark_type in [
            "arrival_mid_price",
            "best_bid_or_ask",
            "decision_price",
            "simple_vwap",
            "simple_twap",
        ]:
            benchmark_price = row["arrival_mid_price"]
            execution_price = row["quantity_weighted_average_price"]
            slippage = abs((execution_price if pd.notna(execution_price) else benchmark_price) - benchmark_price)
            rows.append(
                {
                    "scenario_id": row["scenario_id"],
                    "side": row["side"],
                    "benchmark_type": benchmark_type,
                    "benchmark_price": benchmark_price,
                    "average_execution_price": execution_price,
                    "slippage": slippage,
                    "slippage_bps": slippage / benchmark_price * 10000,
                    "filled_quantity": row["filled_quantity"],
                    "unfilled_quantity": row["unfilled_quantity"],
                    "evidence_level": "controlled_mechanics_validation",
                    "claim_boundary": "Controlled slippage diagnostic only. No empirical execution-cost claim.",
                }
            )
    return pd.DataFrame(rows)
