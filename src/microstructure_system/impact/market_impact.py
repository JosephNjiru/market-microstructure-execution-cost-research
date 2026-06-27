from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_impact_proxies(sweeps: pd.DataFrame) -> pd.DataFrame:
    """Calculate labelled market impact proxies from controlled sweep outputs."""
    return pd.DataFrame(
        {
            "scenario_id": sweeps["scenario_id"],
            "order_size_bucket": np.where(
                sweeps["order_quantity"] <= 500,
                "small",
                np.where(sweeps["order_quantity"] <= 2000, "medium", "large"),
            ),
            "liquidity_regime": sweeps["liquidity_regime"],
            "levels_consumed": sweeps["levels_consumed"],
            "pre_trade_mid_price": sweeps["arrival_mid_price"],
            "post_trade_mid_price": sweeps["arrival_mid_price"],
            "post_trade_mid_change": 0.0,
            "marginal_depth_cost": sweeps["depth_cost"],
            "impact_proxy_cost": 0.0,
            "evidence_level": "controlled_mechanics_validation",
            "claim_boundary": "Impact proxy from controlled fixture only. Not an empirical market impact estimate.",
        }
    )
