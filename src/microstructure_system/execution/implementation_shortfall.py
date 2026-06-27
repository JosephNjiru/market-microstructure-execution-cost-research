from __future__ import annotations

import pandas as pd

from microstructure_system.utils.metadata import ROOT_CLAIM


def calculate_implementation_shortfall(sweeps: pd.DataFrame) -> pd.DataFrame:
    """Calculate implementation shortfall under explicit benchmark assumptions."""
    output = sweeps[
        [
            "scenario_id",
            "side",
            "arrival_mid_price",
            "quantity_weighted_average_price",
            "filled_quantity",
            "unfilled_quantity",
        ]
    ].copy()
    output = output.rename(
        columns={
            "arrival_mid_price": "decision_price",
            "quantity_weighted_average_price": "average_execution_price",
        }
    )
    output["implementation_shortfall"] = (
        output["average_execution_price"] - output["decision_price"]
    ).abs().fillna(0)
    output["implementation_shortfall_bps"] = (
        output["implementation_shortfall"] / output["decision_price"] * 10000
    )
    output["opportunity_cost"] = output["unfilled_quantity"] * output["decision_price"] * 0.0001
    output["total_shortfall_cost"] = (
        output["implementation_shortfall"] * output["filled_quantity"] + output["opportunity_cost"]
    )
    output["evidence_level"] = "controlled_mechanics_validation"
    output["claim_boundary"] = ROOT_CLAIM
    return output
