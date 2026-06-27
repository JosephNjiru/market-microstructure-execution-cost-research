from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.utils.hashing import file_sha256

EXCLUDED_PARTS = {
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "__pycache__",
    "dist",
    "paper",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".bak"}


def build_output_inventory(project_root: Path) -> pd.DataFrame:
    """Build a hashed inventory of current project artefacts."""
    rows = []
    for path in sorted(project_root.rglob("*")):
        if path.is_file() and not _is_excluded_path(path.relative_to(project_root)):
            rows.append(
                {
                    "path": str(path.relative_to(project_root)),
                    "artifact_type": path.suffix or "file",
                    "stage": "current",
                    "size_bytes": path.stat().st_size,
                    "hash": file_sha256(path),
                    "included_in_release": True,
                    "notes": "Current project artefact.",
                }
            )
    return pd.DataFrame(rows)


def build_release_exclusions() -> pd.DataFrame:
    """List release package exclusions."""
    return pd.DataFrame(
        {
            "pattern": [
                ".venv",
                "virtual environments",
                ".pytest_cache",
                ".ruff_cache",
                ".mypy_cache",
                "__pycache__",
                "*.pyc",
                "*.pyo",
                "*.log",
                "*.tmp",
                "*.bak",
                ".env",
                "data/raw",
                "data/external",
                "paper",
                "paid data",
                "account-restricted data",
                "licence-restricted data",
                "large external raw datasets",
            ],
            "reason": [
                "virtual environment",
                "virtual environment",
                "test cache",
                "lint cache",
                "type-check cache",
                "bytecode cache",
                "compiled file",
                "compiled file",
                "log file",
                "temporary file",
                "backup file",
                "environment file",
                "raw external data path",
                "external data path",
                "manual paper draft path",
                "restricted data",
                "restricted data",
                "restricted data",
                "large data",
            ],
            "action": "excluded",
        }
    )


def _is_excluded_path(relative_path: Path) -> bool:
    return (
        any(part in EXCLUDED_PARTS for part in relative_path.parts)
        or relative_path.suffix in EXCLUDED_SUFFIXES
        or relative_path.name == ".env"
    )
