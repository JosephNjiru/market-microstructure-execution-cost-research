from __future__ import annotations

import pandas as pd


def build_known_limitations_register() -> pd.DataFrame:
    """Return the limitations register used by the final report."""
    limitations = [
        "no full L3 data configured",
        "no actual broker execution records",
        "FI-2010 manual download only",
        "LOBSTER sample manual download only",
        "Databento MBO requires account and licence",
        "generated fixtures are mechanics validation only",
        "impact outputs are proxies",
        "limit fill is approximation without L3 data",
        "no best-execution compliance claim",
        "no live-trading claim",
        "no broker-grade TCA claim",
    ]
    return pd.DataFrame(
        [
            {
                "limitation_id": f"LIM-{index:03d}",
                "limitation": limitation,
                "affected_stage": "All",
                "impact": "Limits claim scope.",
                "mitigation": "Add eligible data and independent validation.",
                "status": "active",
            }
            for index, limitation in enumerate(limitations, 1)
        ]
    )


def build_publication_readiness_scorecard() -> pd.DataFrame:
    """Return publication-readiness evidence areas."""
    areas = [
        "research purpose",
        "data capability boundaries",
        "claim enforcement",
        "canonical schemas",
        "feed integrity",
        "order book features",
        "microprice and imbalance",
        "short-horizon labels",
        "baseline diagnostics",
        "execution cost mechanics",
        "slippage benchmarks",
        "schedule diagnostics",
        "fill approximation",
        "cost attribution reconciliation",
        "impact proxy labelling",
        "sensitivity analysis",
        "reproducibility",
        "limitations",
        "release package",
        "manual software paper pathway",
    ]
    return pd.DataFrame(
        {
            "area": areas,
            "status": "ready_with_stated_limits",
            "evidence_path": "reports/tables/publication_readiness_scorecard.csv",
            "notes": "Ready under current evidence scope.",
        }
    )
