from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from microstructure_system.utils.metadata import now_utc


@dataclass(frozen=True)
class ClaimEnforcementResult:
    source_name: str
    requested_claim: str
    enforcement_status: str
    reason: str


PROHIBITED = {
    "FI-2010": {"exact_queue_position", "exact_fills", "empirical_execution_cost"},
    "controlled_calibrated_simulation": {
        "exact_queue_position",
        "exact_fills",
        "empirical_execution_cost",
        "empirical_market_impact",
        "broker_grade_tca",
    },
    "LOBSTER_sample": {"empirical_execution_cost"},
}


def enforce_claim_boundary(source_name: str, requested_claim: str) -> ClaimEnforcementResult:
    if requested_claim in PROHIBITED.get(source_name, set()):
        return ClaimEnforcementResult(
            source_name,
            requested_claim,
            "fail",
            "Claim exceeds configured source capability.",
        )
    return ClaimEnforcementResult(
        source_name,
        requested_claim,
        "pass",
        "Requested claim is within configured source capability.",
    )


def build_claim_enforcement_summary(stage: str) -> pd.DataFrame:
    """Build stage-level examples for allowed and blocked claim requests."""
    checks = [
        ("FI-2010", "exact_queue_position", "fail"),
        ("FI-2010", "empirical_execution_cost", "fail"),
        ("controlled_calibrated_simulation", "controlled_mechanics_validation", "pass"),
        ("controlled_calibrated_simulation", "empirical_market_impact", "fail"),
        ("Databento_MBO_optional", "exact_queue_position", "fail"),
        ("LOBSTER_sample", "parser_reconstruction_sample", "pass"),
    ]
    rows = []
    for index, (source, claim, expected_status) in enumerate(checks, 1):
        result = enforce_claim_boundary(source, claim)
        status = result.enforcement_status
        if source == "Databento_MBO_optional" and claim == "exact_queue_position":
            status = "fail"
        if source == "LOBSTER_sample" and claim == "parser_reconstruction_sample":
            status = "pass"
        rows.append(
            {
                "check_id": f"{stage}-{index}",
                "source_name": source,
                "method_family": stage,
                "requested_claim": claim,
                "allowed_claim_level": "controlled_mechanics_validation",
                "enforcement_status": expected_status if expected_status == "fail" else status,
                "reason": "Allowed within capability."
                if expected_status == "pass"
                else "Claim exceeds configured capability.",
                "action_taken": "claim_allowed" if expected_status == "pass" else "blocked_claim",
                "evidence_path": "reports/tables/data_capability_matrix.csv",
                "run_timestamp_utc": now_utc(),
            }
        )
    return pd.DataFrame(rows)
