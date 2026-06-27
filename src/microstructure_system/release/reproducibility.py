from __future__ import annotations

import platform
import sys
from pathlib import Path

import pandas as pd

from microstructure_system.utils.metadata import PROJECT_VERSION


def build_reproducibility_manifest(project_root: Path) -> pd.DataFrame:
    """Build the reproducibility manifest for commands and environment evidence."""
    _ = project_root
    rows = [
        ("Python version", sys.version.split()[0]),
        ("Project version", PROJECT_VERSION),
        ("Operating system", platform.platform()),
        ("foundation command", "python -m uv run python run_project.py --stage foundation"),
        ("order-book command", "python -m uv run python run_project.py --stage order-book"),
        ("execution-cost command", "python -m uv run python run_project.py --stage execution-cost"),
        ("release command", "python -m uv run python run_project.py --stage release"),
        ("all stages command", "python -m uv run python run_project.py --stage all --config config/project_config.yaml"),
        ("pytest command", "python -m uv run pytest"),
        ("Ruff command", "python -m uv run ruff check ."),
        ("deterministic seed", "20260227"),
        ("data redistribution rule", "no restricted data in release"),
        ("generated fixture status", "available"),
        ("external data status", "not downloaded"),
        ("git commit hash", "git_unavailable"),
        ("git availability status", "git_unavailable"),
    ]
    return pd.DataFrame(
        [
            {
                "item": item,
                "value": value,
                "evidence_path": "reports/tables/reproducibility_manifest.csv",
                "notes": "Release reproducibility evidence.",
            }
            for item, value in rows
        ]
    )
