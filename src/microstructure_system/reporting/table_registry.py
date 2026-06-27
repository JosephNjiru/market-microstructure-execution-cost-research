from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.utils.hashing import file_sha256
from microstructure_system.utils.metadata import NO_CLAIM


def build_table_registry(project_root: Path) -> pd.DataFrame:
    """Register evidence tables across all project stages."""
    rows = []
    for path in sorted((project_root / "reports/tables").glob("*.csv")):
        table = pd.read_csv(path)
        stage = _infer_table_stage(path.name)
        rows.append(
            {
                "table_name": path.name,
                "path": str(path.relative_to(project_root)),
                "stage": stage,
                "row_count": len(table),
                "column_count": len(table.columns),
                "purpose": "Audit evidence table.",
                "evidence_type": "controlled research evidence",
                "claim_boundary": NO_CLAIM,
                "hash": file_sha256(path),
            }
        )
    return pd.DataFrame(rows)


def _infer_table_stage(name: str) -> str:
    if name.startswith(("final", "output", "reproducibility", "known", "publication")):
        return "Stage 4"
    stage3_tokens = [
        "stage3",
        "slippage",
        "impact",
        "sensitivity",
        "shortfall",
        "schedule_execution",
        "limit_order_fill",
        "implementation_shortfall",
        "execution_sensitivity",
    ]
    if any(token in name for token in stage3_tokens):
        return "Stage 3"
    stage2_tokens = [
        "stage2",
        "feature",
        "microprice",
        "liquidity",
        "label",
        "imbalance",
        "event_intensity",
        "intraday",
        "baseline_model",
        "order_book_feature",
    ]
    if any(token in name for token in stage2_tokens):
        return "Stage 2"
    return "Stage 1"
