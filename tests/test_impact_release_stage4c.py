from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from microstructure_system.impact.market_impact import calculate_impact_proxies
from microstructure_system.impact.sensitivity import build_execution_sensitivity_summary
from microstructure_system.release.manifest import build_release_exclusions


def test_impact_proxy_labelling(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, _, _ = sweep_outputs
    impact = calculate_impact_proxies(sweep)
    assert impact["claim_boundary"].str.contains("Impact proxy").all()


def test_sensitivity_is_deterministic(
    sweep_outputs: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
) -> None:
    sweep, _, _ = sweep_outputs
    pd.testing.assert_frame_equal(
        build_execution_sensitivity_summary(sweep),
        build_execution_sensitivity_summary(sweep),
    )


def test_release_exclusions_cover_public_cleanliness_requirements() -> None:
    patterns = set(build_release_exclusions()["pattern"])
    assert {".venv", ".pytest_cache", ".ruff_cache", ".mypy_cache", "__pycache__", ".env"}.issubset(patterns)


def test_release_zip_excludes_environment_and_cache_paths() -> None:
    package = Path("dist/market_microstructure_execution_cost_system_source_release.zip")
    with ZipFile(package) as archive:
        names = archive.namelist()
    joined = "\n".join(names)
    assert ".venv" not in joined
    assert "__pycache__" not in joined
