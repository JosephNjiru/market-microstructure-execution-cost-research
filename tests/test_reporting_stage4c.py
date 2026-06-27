from __future__ import annotations

from pathlib import Path

from microstructure_system.reporting.claim_boundary_audit import build_claim_boundary_audit
from microstructure_system.reporting.figure_registry import build_figure_registry
from microstructure_system.reporting.table_registry import build_table_registry


def test_final_report_contains_required_stage4c_sections() -> None:
    text = Path("reports/market_microstructure_execution_cost_report.md").read_text(encoding="utf-8")
    for heading in [
        "Author: Joseph N. Njiru",
        "## Evidence boundary",
        "## Claim enforcement design",
        "## Implementation shortfall",
        "## Release package contents",
    ]:
        assert heading in text


def test_public_report_notes_manual_paper_pathway() -> None:
    text = Path("reports/market_microstructure_execution_cost_report.md").read_text(encoding="utf-8")
    assert "software paper and full bibliography will be finalised manually" in text.lower()


def test_registries_cover_all_stages() -> None:
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(
        set(build_table_registry(Path.cwd())["stage"])
    )
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(
        set(build_figure_registry(Path.cwd())["stage"])
    )


def test_table_registry_labels_stage_specific_outputs() -> None:
    registry = build_table_registry(Path.cwd()).set_index("table_name")
    assert registry.loc["baseline_model_performance.csv", "stage"] == "Stage 2"
    assert registry.loc["event_intensity_summary.csv", "stage"] == "Stage 2"
    assert registry.loc["schedule_execution_summary.csv", "stage"] == "Stage 3"
    assert registry.loc["limit_order_fill_approximation_summary.csv", "stage"] == "Stage 3"


def test_claim_boundary_audit_has_zero_fail_rows() -> None:
    audit = build_claim_boundary_audit()
    assert not (audit["claim_status"] == "fail").any()
