from __future__ import annotations

import pandas as pd

from microstructure_system.schemas.validation import (
    build_schema_validation_summary,
    validate_named_frame,
)
from microstructure_system.simulation.lob_fixture import (
    generate_stage1_execution_scenarios,
    generate_tiny_order_events,
    generate_tiny_trade_events,
)


def test_schema_summary_contains_requested_names() -> None:
    summary = build_schema_validation_summary(["BookSnapshotL2", "ExecutionScenario"])
    assert list(summary["schema_name"]) == ["BookSnapshotL2", "ExecutionScenario"]
    assert set(summary["status"]) == {"pass"}


def test_schema_validation_rejects_unknown_schema(tiny_book: pd.DataFrame) -> None:
    assert validate_named_frame("UnknownSchema", tiny_book)["status"] == "fail"


def test_fixture_generates_scenarios_events_and_trades(tiny_book: pd.DataFrame) -> None:
    scenarios = generate_stage1_execution_scenarios(tiny_book)
    events = generate_tiny_order_events(tiny_book)
    trades = generate_tiny_trade_events(tiny_book)
    assert len(scenarios) == 4
    assert len(events) == 5
    assert len(trades) == 5
