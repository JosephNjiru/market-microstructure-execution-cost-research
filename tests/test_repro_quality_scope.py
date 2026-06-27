from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.quality.final_quality import build_final_quality_gate
from microstructure_system.release.reproducibility import build_reproducibility_manifest


def test_reproducibility_manifest_records_required_commands() -> None:
    manifest = build_reproducibility_manifest(Path.cwd())
    items = set(manifest["item"])
    assert {"foundation command", "order-book command", "execution-cost command", "release command"}.issubset(items)


def test_final_quality_gate_has_no_failures() -> None:
    gate = build_final_quality_gate(Path.cwd())
    assert set(gate["status"]) == {"pass"}


def test_stage_scope_does_not_create_unrequested_release_files() -> None:
    assert not Path("paper/final_peer_review_article.md").exists()
    assert not Path("reports/final_peer_review_article.html").exists()


def test_generated_outputs_remain_mechanics_validation_only() -> None:
    costs = pd.read_parquet("data/processed/stage3_cost_attribution.parquet")
    assert costs["data_quality_flag"].eq("generated_controlled").all()
