from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.quality.stage1_quality import _quality_gate


def build_stage3_quality_gate(project_root: Path) -> pd.DataFrame:
    """Build the Stage 3 quality gate table."""
    return _quality_gate(
        "Stage 3",
        project_root,
        ["stage3_sweep_summary.csv", "stage3_claim_enforcement_summary.csv"],
    )
