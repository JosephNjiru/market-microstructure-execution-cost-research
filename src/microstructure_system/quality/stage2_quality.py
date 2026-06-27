from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.quality.stage1_quality import _quality_gate


def build_stage2_quality_gate(project_root: Path) -> pd.DataFrame:
    """Build the Stage 2 quality gate table."""
    return _quality_gate(
        "Stage 2",
        project_root,
        ["order_book_feature_summary.csv", "stage2_claim_enforcement_summary.csv"],
    )
