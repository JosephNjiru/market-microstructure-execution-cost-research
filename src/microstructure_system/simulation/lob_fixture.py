from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd

from microstructure_system.utils.hashing import add_record_hashes
from microstructure_system.utils.metadata import GENERATED_FIXTURE_INGESTED_AT


def generate_tiny_lob_fixture() -> pd.DataFrame:
    """Create the deterministic L2 book fixture used for controlled validation."""
    rows: list[dict[str, object]] = []
    base = datetime(2026, 1, 2, 9, 30, tzinfo=UTC)
    for index in range(15):
        spread = 0.02 if index < 5 else 0.04
        if index == 10:
            spread = 0.0
        if index == 11:
            spread = -0.02
        mid = 100 + (index % 3) * 0.01
        row: dict[str, object] = {
            "timestamp_utc": base + timedelta(seconds=index if index != 13 else 2),
            "sequence_number": index + 1,
            "tick_size": 0.01,
            "lot_size": 100,
            "auction_or_halt_flag": index == 6,
            "source": "controlled_calibrated_simulation",
            "source_dataset": "tiny_stage1_lob_fixture",
            "ingested_at_utc": GENERATED_FIXTURE_INGESTED_AT,
            "schema_version": "restored.1",
            "data_quality_flag": "valid",
        }
        for level in range(1, 6):
            row[f"bid_price_{level}"] = round(mid - spread / 2 - (level - 1) * 0.01, 2)
            row[f"ask_price_{level}"] = round(mid + spread / 2 + (level - 1) * 0.01, 2)
            size = 100 if index in {8, 9} else 500
            row[f"bid_size_{level}"] = float(size + 100 * level)
            row[f"ask_size_{level}"] = float(size + 100 * level)
        if index == 14:
            row["bid_price_5"] = np.nan
        rows.append(row)
    return add_record_hashes(pd.DataFrame(rows))


def generate_stage1_execution_scenarios(book: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic Stage 1 marketable-order scenarios."""
    timestamp = book.loc[2, "timestamp_utc"]
    scenarios = pd.DataFrame(
        [
            {
                "scenario_id": "marketable_buy",
                "timestamp_utc": timestamp,
                "side": "buy",
                "order_quantity": 700.0,
                "limit_price": np.nan,
                "partial_fill_allowed": True,
                "schedule_type": "market_sweep",
            },
            {
                "scenario_id": "marketable_sell",
                "timestamp_utc": timestamp,
                "side": "sell",
                "order_quantity": 700.0,
                "limit_price": np.nan,
                "partial_fill_allowed": True,
                "schedule_type": "market_sweep",
            },
            {
                "scenario_id": "partial_fill_buy_limit",
                "timestamp_utc": book.loc[8, "timestamp_utc"],
                "side": "buy",
                "order_quantity": 2600.0,
                "limit_price": 100.03,
                "partial_fill_allowed": True,
                "schedule_type": "market_sweep",
            },
            {
                "scenario_id": "unfilled_residual_buy_limit",
                "timestamp_utc": book.loc[8, "timestamp_utc"],
                "side": "buy",
                "order_quantity": 5000.0,
                "limit_price": 100.01,
                "partial_fill_allowed": True,
                "schedule_type": "market_sweep",
            },
        ]
    )
    return add_record_hashes(
        scenarios.assign(
            source="controlled_calibrated_simulation",
            source_dataset="tiny_stage1_lob_fixture",
            ingested_at_utc=GENERATED_FIXTURE_INGESTED_AT,
            schema_version="restored.1",
            data_quality_flag="generated_controlled",
        )
    )


def generate_tiny_order_events(book: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic L3-shaped sample events for parser schema checks."""
    return add_record_hashes(
        pd.DataFrame(
            {
                "timestamp_utc": book["timestamp_utc"].head(5),
                "sequence_number": range(1, 6),
                "order_id": [f"ORD{index}" for index in range(5)],
                "event_type": "add",
                "side": "buy",
                "price": 100.0,
                "quantity": 100.0,
                "source": "controlled_calibrated_simulation",
                "source_dataset": "tiny_stage1_lob_fixture",
                "ingested_at_utc": GENERATED_FIXTURE_INGESTED_AT,
                "schema_version": "restored.1",
                "data_quality_flag": "generated_controlled",
            }
        )
    )


def generate_tiny_trade_events(book: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic trade-shaped sample rows for schema checks."""
    return add_record_hashes(
        pd.DataFrame(
            {
                "timestamp_utc": book["timestamp_utc"].head(5),
                "trade_id": [f"TRD{index}" for index in range(5)],
                "side": "buy",
                "price": 100.01,
                "quantity": 100.0,
                "source": "controlled_calibrated_simulation",
                "source_dataset": "tiny_stage1_lob_fixture",
                "ingested_at_utc": GENERATED_FIXTURE_INGESTED_AT,
                "schema_version": "restored.1",
                "data_quality_flag": "generated_controlled",
            }
        )
    )
