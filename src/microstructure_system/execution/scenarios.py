from __future__ import annotations

import numpy as np
import pandas as pd

from microstructure_system.utils.hashing import add_record_hashes
from microstructure_system.utils.metadata import GENERATED_FIXTURE_INGESTED_AT, ROOT_CLAIM


def generate_stage3_execution_scenarios(features: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic Stage 3 execution scenarios from valid L2 features."""
    scenario_rows = [
        ("market_sweep_small", 300.0, np.nan, "market_sweep"),
        ("market_sweep_medium", 1200.0, np.nan, "market_sweep"),
        ("market_sweep_large", 5000.0, np.nan, "market_sweep"),
        ("market_sweep_sell_medium", 1200.0, np.nan, "market_sweep"),
        ("market_sweep_partial_fill", 2600.0, 100.03, "market_sweep"),
        ("market_sweep_unfilled_residual", 5000.0, 100.01, "market_sweep"),
        ("wide_spread_sweep", 1200.0, np.nan, "market_sweep"),
        ("vwap_schedule", 2400.0, np.nan, "vwap"),
        ("twap_schedule", 2400.0, np.nan, "twap"),
        ("participation_schedule", 2400.0, np.nan, "participation"),
        ("limit_order_fill_approximation", 1200.0, 99.99, "limit_order"),
    ]
    valid_features = features[features["valid_feature_row"]]
    output = []
    for index, (scenario_id, quantity, limit_price, schedule_type) in enumerate(scenario_rows):
        feature = valid_features.iloc[min(index, 8)]
        output.append(
            {
                "scenario_id": scenario_id,
                "timestamp_utc": feature["timestamp_utc"],
                "side": "sell" if "sell" in scenario_id else "buy",
                "order_quantity": quantity,
                "limit_price": limit_price,
                "participation_rate": 0.2,
                "schedule_type": schedule_type,
                "benchmark_type": "arrival_mid_price",
                "arrival_mid_price": feature["mid_price"],
                "arrival_best_bid": feature["best_bid_price"],
                "arrival_best_ask": feature["best_ask_price"],
                "arrival_spread": feature["quoted_spread"],
                "liquidity_regime": feature["liquidity_regime"],
                "source": "controlled_calibrated_simulation",
                "source_dataset": "tiny_stage1_lob_fixture",
                "evidence_level": "controlled_mechanics_validation",
                "claim_boundary": ROOT_CLAIM,
                "ingested_at_utc": GENERATED_FIXTURE_INGESTED_AT,
                "schema_version": "restored.1",
                "data_quality_flag": "generated_controlled",
            }
        )
    return add_record_hashes(pd.DataFrame(output))
