from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


def test_final_quality_gate_passes() -> None:
    gate = pd.read_csv("reports/tables/final_quality_gate.csv")
    assert not gate.empty
    assert (gate["status"] == "pass").all()


def test_claim_boundary_audit_has_no_failures() -> None:
    audit = pd.read_csv("reports/tables/final_claim_boundary_audit.csv")
    assert not audit.empty
    assert not (audit["claim_status"] == "fail").any()


def test_public_reports_exist_without_manual_paper_folder() -> None:
    for path in [
        "reports/market_microstructure_execution_cost_report.md",
        "reports/market_microstructure_execution_cost_report.html",
    ]:
        assert Path(path).exists(), path


def test_registries_cover_all_stages() -> None:
    tables = pd.read_csv("reports/tables/final_table_registry.csv")
    figures = pd.read_csv("reports/tables/final_figure_registry.csv")
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(set(tables["stage"]))
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(set(figures["stage"]))


def test_reproducibility_and_limitations_are_recorded() -> None:
    manifest = pd.read_csv("reports/tables/reproducibility_manifest.csv")
    limitations = pd.read_csv("reports/tables/known_limitations_register.csv")
    assert "all stages command" in set(manifest["item"])
    assert len(limitations) >= 11


def test_release_package_exists_and_excludes_clutter() -> None:
    package = Path("dist/market_microstructure_execution_cost_system_source_release.zip")
    assert package.exists()
    with ZipFile(package) as archive:
        names = archive.namelist()
    assert "README.md" in names
    assert "pyproject.toml" in names
    assert any(name.startswith("src/") for name in names)
    assert any(name.startswith("tests/") for name in names)
    joined = "\n".join(names)
    assert ".venv" not in joined
    assert "__pycache__" not in joined
    assert ".pytest_cache" not in joined
    assert ".ruff_cache" not in joined


def test_no_prohibited_affirmative_claims() -> None:
    text = "\n".join(
        Path(path).read_text(encoding="utf-8").lower()
        for path in [
            "README.md",
            "reports/market_microstructure_execution_cost_report.md",
        ]
    )
    for phrase in [
        "profitable trading system",
        "live trading ready",
        "best-execution compliant",
        "broker-grade transaction cost analysis",
        "institutional execution quality",
    ]:
        assert phrase not in text
