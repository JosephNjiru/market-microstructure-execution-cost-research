from __future__ import annotations

from microstructure_system.data.source_audit import (
    build_data_capability_matrix,
    run_data_source_audit,
)


def test_capability_matrix_has_required_claim_columns() -> None:
    matrix = build_data_capability_matrix()
    required = {
        "supports_queue_position",
        "supports_exact_fills",
        "supports_empirical_execution_cost_claims",
        "allowed_claim_level",
        "prohibited_claims",
    }
    assert required.issubset(matrix.columns)


def test_fi2010_boundary_blocks_execution_claims() -> None:
    fi = build_data_capability_matrix().set_index("source_name").loc["FI-2010"]
    assert fi["allowed_claim_level"] == "lob_feature_benchmark"
    assert not bool(fi["supports_exact_fills"])
    assert "empirical_execution_cost" in fi["prohibited_claims"]


def test_source_audit_keeps_external_data_out_of_public_release() -> None:
    audit = run_data_source_audit().set_index("source_name")
    assert audit.loc["Databento_MBO_optional", "requires_account"]
    assert audit.loc["LOBSTER_sample", "requires_manual_download"]
    assert audit.loc["controlled_calibrated_simulation", "download_success"]
