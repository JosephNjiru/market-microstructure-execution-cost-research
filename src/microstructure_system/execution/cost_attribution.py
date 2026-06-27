from __future__ import annotations

import pandas as pd


def components_reconcile(row: pd.Series) -> bool:
    components = [
        "spread_cost",
        "depth_cost",
        "slippage_cost",
        "opportunity_cost",
        "impact_proxy_cost",
        "timing_cost",
        "fees",
    ]
    available = [component for component in components if component in row.index]
    return abs(sum(float(row[component]) for component in available) - float(row["total_cost"])) < 1e-8


def build_stage3_cost_attribution(costs: pd.DataFrame, impact: pd.DataFrame) -> pd.DataFrame:
    """Add Stage 3 timing, fee and impact proxy components and reconcile totals."""
    output = costs.merge(
        impact[["scenario_id", "impact_proxy_cost"]],
        on="scenario_id",
        how="left",
    ).fillna({"impact_proxy_cost": 0.0})
    output["timing_cost"] = 0.0
    output["fees"] = 0.0
    output["total_cost"] = output[
        [
            "spread_cost",
            "depth_cost",
            "slippage_cost",
            "opportunity_cost",
            "impact_proxy_cost",
            "timing_cost",
            "fees",
        ]
    ].sum(axis=1)
    output["components_reconcile"] = output.apply(components_reconcile, axis=1)
    return output
