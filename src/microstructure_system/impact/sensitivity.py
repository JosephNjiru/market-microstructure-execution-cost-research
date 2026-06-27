from __future__ import annotations

import numpy as np
import pandas as pd


def build_execution_sensitivity_summary(sweeps: pd.DataFrame) -> pd.DataFrame:
    """Build deterministic sensitivity summaries over controlled sweep outputs."""
    rows = []
    variables = {
        "order_size_bucket": np.where(
            sweeps["order_quantity"] <= 500,
            "small",
            np.where(sweeps["order_quantity"] <= 2000, "medium", "large"),
        ),
        "spread_regime": sweeps["liquidity_regime"],
        "fee_assumption": ["0.0"] * len(sweeps),
    }
    for variable_name, values in variables.items():
        frame = sweeps.assign(variable_value=values)
        for value, group in frame.groupby("variable_value"):
            rows.append(
                {
                    "sensitivity_id": f"{variable_name}_{value}",
                    "variable_name": variable_name,
                    "variable_value": value,
                    "scenario_count": len(group),
                    "mean_cost_bps": group["cost_bps"].mean(),
                    "median_cost_bps": group["cost_bps"].median(),
                    "max_cost_bps": group["cost_bps"].max(),
                    "partial_fill_count": int((group["execution_status"] == "partial_fill").sum()),
                    "unfilled_count": int((group["unfilled_quantity"] > 0).sum()),
                    "evidence_level": "controlled_mechanics_validation",
                    "claim_boundary": "Controlled sensitivity diagnostic only. No empirical execution-cost claim.",
                }
            )
    return pd.DataFrame(rows)
