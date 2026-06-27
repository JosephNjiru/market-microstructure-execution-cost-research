from __future__ import annotations

import pandas as pd


def approximate_limit_order_fills(scenarios: pd.DataFrame) -> pd.DataFrame:
    """Approximate limit-order fills from L2 data without claiming exact fills."""
    scenario = scenarios[scenarios["schedule_type"] == "limit_order"].iloc[0]
    return pd.DataFrame(
        [
            {
                "scenario_id": scenario["scenario_id"],
                "side": scenario["side"],
                "limit_price": scenario["limit_price"],
                "order_quantity": scenario["order_quantity"],
                "approx_filled_quantity": 0.0,
                "approx_unfilled_quantity": scenario["order_quantity"],
                "approx_fill_status": "not_filled_approximation",
                "requires_l3_for_exact_claim": True,
                "evidence_level": "controlled_mechanics_validation",
                "claim_boundary": "Approximation from L2 only. Exact fill claims require L3 order IDs and queue data.",
            }
        ]
    )
