from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

ROOT_CLAIM = "Controlled mechanics validation only. No empirical execution-cost claim."
NO_CLAIM = "No trading, profitability, best-execution, live-trading or broker-grade TCA claim."
GENERATED_FIXTURE_INGESTED_AT = "2026-01-02T00:00:00+00:00"
PROJECT_VERSION = "0.1.0"


def now_utc() -> str:
    """Return an ISO 8601 UTC timestamp for run metadata."""
    return datetime.now(UTC).isoformat()


def ensure_project_directories(project_root: Path) -> None:
    """Create the output directories used by the four-stage pipeline."""
    for relative_path in [
        "data/generated",
        "data/processed",
        "reports/tables",
        "reports/figures",
        "paper",
        "dist",
    ]:
        (project_root / relative_path).mkdir(parents=True, exist_ok=True)
