from __future__ import annotations

import pandas as pd

from microstructure_system.features.event_intensity import compute_event_intensity
from microstructure_system.features.labels import summarise_label_distribution
from microstructure_system.models.baselines import run_baseline_models


def test_label_distribution_preserves_claim_boundary(short_horizon_labels: pd.DataFrame) -> None:
    summary = summarise_label_distribution(short_horizon_labels)
    assert summary["claim_boundary"].str.contains("No execution-cost claim").all()


def test_event_intensity_uses_low_activity_period_name(tiny_book: pd.DataFrame) -> None:
    intensity = compute_event_intensity(tiny_book)
    assert "low_activity_period_flag" in intensity.columns
    assert "quiet_period_flag" not in intensity.columns


def test_baseline_models_are_controlled_fixture_diagnostics(short_horizon_labels: pd.DataFrame) -> None:
    models = run_baseline_models(short_horizon_labels)
    assert set(models["model_evidence_level"]) == {"controlled_fixture_diagnostic"}
