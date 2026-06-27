from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.utils.hashing import file_sha256
from microstructure_system.utils.metadata import NO_CLAIM


def build_figure_registry(project_root: Path) -> pd.DataFrame:
    """Register evidence figures across all project stages."""
    rows = []
    for path in sorted((project_root / "reports/figures").glob("*.png")):
        rows.append(
            {
                "figure_name": path.name,
                "path": str(path.relative_to(project_root)),
                "stage": _infer_figure_stage(path.name),
                "purpose": path.stem.replace("_", " "),
                "evidence_type": "controlled diagnostic visual evidence",
                "claim_boundary": NO_CLAIM,
                "hash": file_sha256(path),
            }
        )
    return pd.DataFrame(rows)


def _infer_figure_stage(name: str) -> str:
    if name.startswith("final_"):
        return "Stage 4"
    if any(token in name for token in ["execution", "slippage", "shortfall", "waterfall", "sensitivity"]):
        return "Stage 3"
    if any(token in name for token in ["microprice", "liquidity", "label", "imbalance", "spread_through"]):
        return "Stage 2"
    return "Stage 1"
