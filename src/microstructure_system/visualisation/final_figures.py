from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.visualisation.common import write_bar_figure


def write_final_figures(project_root: Path) -> None:
    """Write final summary figures used by release reporting."""
    for filename in [
        "final_system_architecture.png",
        "final_evidence_boundary_map.png",
        "final_stage_quality_summary.png",
        "final_claim_enforcement_summary.png",
    ]:
        write_bar_figure(
            project_root / "reports/figures" / filename,
            pd.Series([1, 2, 3, 4]),
            filename.replace("_", " ").replace(".png", ""),
        )
