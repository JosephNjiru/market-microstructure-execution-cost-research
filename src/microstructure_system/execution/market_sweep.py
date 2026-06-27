from __future__ import annotations

import numpy as np
import pandas as pd

from microstructure_system.utils.hashing import add_record_hashes
from microstructure_system.utils.metadata import GENERATED_FIXTURE_INGESTED_AT, ROOT_CLAIM


def run_market_sweeps(
    book: pd.DataFrame,
    scenarios: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run L2 marketable-order sweeps across displayed book levels."""
    summaries: list[dict[str, object]] = []
    fills: list[dict[str, object]] = []
    for _, scenario in scenarios.iterrows():
        snapshot = book[
            pd.to_datetime(book["timestamp_utc"], utc=True)
            == pd.to_datetime(scenario["timestamp_utc"], utc=True)
        ].iloc[0]
        side = scenario["side"]
        remaining = float(scenario["order_quantity"])
        consumed_levels: list[tuple[int, float, float, float]] = []
        for level in range(1, 6):
            side_prefix = "ask" if side == "buy" else "bid"
            price = float(snapshot[f"{side_prefix}_price_{level}"])
            limit_price = scenario["limit_price"]
            if pd.notna(limit_price) and (
                (side == "buy" and price > limit_price)
                or (side == "sell" and price < limit_price)
            ):
                continue
            quantity = min(float(snapshot[f"{side_prefix}_size_{level}"]), remaining)
            if quantity <= 0:
                continue
            remaining -= quantity
            consumed_levels.append((level, price, quantity, remaining))
            if remaining <= 0:
                break
        filled = float(scenario["order_quantity"]) - remaining
        notional = sum(price * quantity for _, price, quantity, _ in consumed_levels)
        qwap = np.nan if filled == 0 else notional / filled
        mid = (snapshot["bid_price_1"] + snapshot["ask_price_1"]) / 2
        spread = snapshot["ask_price_1"] - snapshot["bid_price_1"]
        spread_cost = filled * max(spread, 0) / 2
        depth_cost = max(
            0.0,
            notional - filled * (snapshot["ask_price_1"] if side == "buy" else snapshot["bid_price_1"]),
        )
        if side == "sell":
            depth_cost = max(0.0, filled * snapshot["bid_price_1"] - notional)
        opportunity_cost = remaining * max(spread, 0) / 2
        total_cost = spread_cost + depth_cost + opportunity_cost
        summaries.append(
            {
                "scenario_id": scenario["scenario_id"],
                "side": side,
                "order_quantity": scenario["order_quantity"],
                "filled_quantity": filled,
                "unfilled_quantity": remaining,
                "quantity_weighted_average_price": qwap,
                "arrival_mid_price": mid,
                "arrival_spread": spread,
                "execution_status": "filled" if remaining == 0 else "partial_fill",
                "levels_consumed": len(consumed_levels),
                "gross_notional": notional,
                "spread_cost": spread_cost,
                "depth_cost": depth_cost,
                "slippage_cost": 0.0,
                "opportunity_cost": opportunity_cost,
                "total_cost": total_cost,
                "cost_bps": 0 if mid == 0 else total_cost / (mid * scenario["order_quantity"]) * 10000,
                "liquidity_regime": scenario.get("liquidity_regime", "normal"),
                "evidence_level": "controlled_mechanics_validation",
                "claim_boundary": ROOT_CLAIM,
            }
        )
        for sequence, (level, price, quantity, remaining_after_level) in enumerate(consumed_levels, 1):
            fills.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "timestamp_utc": scenario["timestamp_utc"],
                    "side": side,
                    "level": level,
                    "price": price,
                    "quantity_filled": quantity,
                    "level_notional": price * quantity,
                    "remaining_quantity_after_level": remaining_after_level,
                    "fill_sequence": sequence,
                    "fill_status": "final_level" if remaining_after_level == 0 else "filled_level",
                    "source": "controlled_calibrated_simulation",
                    "source_dataset": "tiny_stage1_lob_fixture",
                    "evidence_level": "controlled_mechanics_validation",
                    "claim_boundary": ROOT_CLAIM,
                }
            )
    sweep = pd.DataFrame(summaries)
    costs = add_record_hashes(
        sweep[
            [
                "scenario_id",
                "side",
                "spread_cost",
                "depth_cost",
                "slippage_cost",
                "opportunity_cost",
                "total_cost",
            ]
        ].assign(
            source="controlled_calibrated_simulation",
            source_dataset="tiny_stage1_lob_fixture",
            ingested_at_utc=GENERATED_FIXTURE_INGESTED_AT,
            schema_version="restored.1",
            data_quality_flag="generated_controlled",
            components_reconcile=True,
        )
    )
    return sweep, add_record_hashes(pd.DataFrame(fills)), costs
