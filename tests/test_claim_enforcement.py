from __future__ import annotations

from microstructure_system.quality.claim_enforcement import (
    build_claim_enforcement_summary,
    enforce_claim_boundary,
)


def test_claim_enforcement_blocks_fi2010_exact_queue_position() -> None:
    result = enforce_claim_boundary("FI-2010", "exact_queue_position")
    assert result.enforcement_status == "fail"


def test_claim_enforcement_blocks_generated_empirical_market_impact() -> None:
    result = enforce_claim_boundary("controlled_calibrated_simulation", "empirical_market_impact")
    assert result.enforcement_status == "fail"


def test_claim_enforcement_summary_records_blocked_actions() -> None:
    summary = build_claim_enforcement_summary("release")
    assert "blocked_claim" in set(summary["action_taken"])
    assert "claim_allowed" in set(summary["action_taken"])
