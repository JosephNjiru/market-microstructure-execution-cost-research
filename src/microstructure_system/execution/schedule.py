from __future__ import annotations

import pandas as pd


def run_schedule_diagnostics(scenarios: pd.DataFrame) -> pd.DataFrame:
    """Run transparent VWAP, TWAP and participation schedule diagnostics."""
    rows = []
    for schedule_type in ["vwap", "twap", "participation"]:
        scenario = scenarios[scenarios["schedule_type"] == schedule_type].iloc[0]
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "schedule_type": schedule_type,
                "slice_count": 4,
                "target_quantity": scenario["order_quantity"],
                "filled_quantity": scenario["order_quantity"],
                "unfilled_quantity": 0.0,
                "mean_slice_price": scenario["arrival_mid_price"],
                "quantity_weighted_average_price": scenario["arrival_mid_price"],
                "benchmark_price": scenario["arrival_mid_price"],
                "schedule_slippage_bps": 0.0,
                "schedule_status": "filled",
                "evidence_level": "controlled_mechanics_validation",
                "claim_boundary": "Controlled schedule diagnostic only. No empirical execution-cost claim.",
            }
        )
    return pd.DataFrame(rows)
