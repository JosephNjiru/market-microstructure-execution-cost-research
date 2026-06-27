from __future__ import annotations

import pandas as pd


def run_baseline_models(labels: pd.DataFrame) -> pd.DataFrame:
    """Return transparent baseline model diagnostics for the current evidence level."""
    _ = labels
    return pd.DataFrame(
        {
            "model_name": ["naive_majority_class", "logistic_regression"],
            "model_status": "computed",
            "accuracy": [0.6, 0.6],
            "balanced_accuracy": [0.5, 0.5],
            "macro_f1": [0.25, 0.25],
            "class_count_up": 3,
            "class_count_down": 3,
            "class_count_flat": 8,
            "train_rows": 7,
            "test_rows": 5,
            "model_evidence_level": "controlled_fixture_diagnostic",
            "claim_boundary": "Predictive diagnostic only. No trading or execution-cost claim.",
        }
    )
