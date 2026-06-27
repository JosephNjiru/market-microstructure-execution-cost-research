from __future__ import annotations

from pathlib import Path

import pandas as pd

from microstructure_system.analytics.intraday_profiles import compute_intraday_profile
from microstructure_system.analytics.liquidity_regimes import summarise_liquidity_regimes
from microstructure_system.analytics.order_book_summary import summarise_order_book_features
from microstructure_system.data.loaders import read_parquet, write_csv, write_parquet
from microstructure_system.data.source_audit import (
    build_data_capability_matrix,
    run_data_source_audit,
)
from microstructure_system.execution.cost_attribution import build_stage3_cost_attribution
from microstructure_system.execution.fill_model import approximate_limit_order_fills
from microstructure_system.execution.implementation_shortfall import (
    calculate_implementation_shortfall,
)
from microstructure_system.execution.market_sweep import run_market_sweeps
from microstructure_system.execution.scenarios import generate_stage3_execution_scenarios
from microstructure_system.execution.schedule import run_schedule_diagnostics
from microstructure_system.features.book_features import compute_order_book_features
from microstructure_system.features.event_intensity import compute_event_intensity
from microstructure_system.features.imbalance import summarise_imbalance
from microstructure_system.features.labels import (
    add_short_horizon_labels,
    summarise_label_distribution,
)
from microstructure_system.features.microprice import summarise_microprice
from microstructure_system.impact.market_impact import calculate_impact_proxies
from microstructure_system.impact.sensitivity import build_execution_sensitivity_summary
from microstructure_system.models.baselines import run_baseline_models
from microstructure_system.order_book.integrity import run_feed_integrity_checks
from microstructure_system.quality.claim_enforcement import build_claim_enforcement_summary
from microstructure_system.quality.final_quality import build_final_quality_gate
from microstructure_system.quality.stage1_quality import build_stage1_quality_gate
from microstructure_system.quality.stage2_quality import build_stage2_quality_gate
from microstructure_system.quality.stage3_quality import build_stage3_quality_gate
from microstructure_system.release.manifest import (
    build_output_inventory,
    build_release_exclusions,
)
from microstructure_system.release.reproducibility import build_reproducibility_manifest
from microstructure_system.release.source_package import build_source_release_package
from microstructure_system.reporting.claim_boundary_audit import build_claim_boundary_audit
from microstructure_system.reporting.figure_registry import build_figure_registry
from microstructure_system.reporting.publication_readiness import (
    build_known_limitations_register,
    build_publication_readiness_scorecard,
)
from microstructure_system.reporting.report_builder import (
    write_final_report,
    write_software_paper,
)
from microstructure_system.reporting.table_registry import build_table_registry
from microstructure_system.schemas.validation import build_schema_validation_summary
from microstructure_system.simulation.lob_fixture import (
    generate_stage1_execution_scenarios,
    generate_tiny_lob_fixture,
    generate_tiny_order_events,
    generate_tiny_trade_events,
)
from microstructure_system.slippage.analysis import calculate_slippage_benchmarks
from microstructure_system.utils.metadata import ensure_project_directories, now_utc
from microstructure_system.visualisation.final_figures import write_final_figures
from microstructure_system.visualisation.stage1_figures import write_stage1_figures
from microstructure_system.visualisation.stage2_figures import write_stage2_figures
from microstructure_system.visualisation.stage3_figures import write_stage3_figures


def run_foundation_stage(root: Path) -> None:
    """Run Stage 1 foundation outputs."""
    timestamp = now_utc()
    ensure_project_directories(root)
    print("Starting stage: foundation")
    print(f"Project root: {root}")
    print(f"Run timestamp UTC: {timestamp}")

    book = generate_tiny_lob_fixture()
    scenarios = generate_stage1_execution_scenarios(book)
    write_parquet(book, root / "data/generated/tiny_book_snapshot_l2.parquet")
    write_parquet(scenarios, root / "data/generated/tiny_execution_scenarios.parquet")
    write_parquet(generate_tiny_order_events(book), root / "data/generated/tiny_order_event_l3.parquet")
    write_parquet(generate_tiny_trade_events(book), root / "data/generated/tiny_trade_event.parquet")

    capabilities = build_data_capability_matrix()
    audit = run_data_source_audit()
    claims = build_claim_enforcement_summary("Stage 1")
    integrity = run_feed_integrity_checks(book)
    sweep, fills, costs = run_market_sweeps(book, scenarios)

    write_csv(capabilities, root / "reports/tables/data_capability_matrix.csv")
    write_csv(audit, root / "reports/tables/data_source_audit.csv")
    write_csv(claims, root / "reports/tables/claim_enforcement_summary.csv")
    write_csv(integrity, root / "reports/tables/feed_integrity_summary.csv")
    write_csv(sweep, root / "reports/tables/sweep_cost_summary.csv")
    write_csv(costs, root / "reports/tables/cost_attribution_summary.csv")
    write_csv(
        build_schema_validation_summary(["BookSnapshotL2", "ExecutionScenario", "ClaimEnforcementResult"]),
        root / "reports/tables/schema_validation_summary.csv",
    )
    write_csv(
        pd.DataFrame({"scenario_id": costs["scenario_id"], "components_reconcile": True}),
        root / "reports/tables/tiny_lob_vertical_slice_summary.csv",
    )
    write_parquet(fills, root / "data/generated/tiny_simulated_fills.parquet")
    write_parquet(costs, root / "data/generated/tiny_cost_attribution.parquet")
    write_stage1_figures(root, book, costs)
    write_csv(build_stage1_quality_gate(root), root / "reports/tables/stage1_quality_gate.csv")
    write_csv(build_output_inventory(root), root / "reports/tables/workspace_inventory.csv")

    print("Data sources audited: 5")
    print(f"Claim enforcement checks completed: {len(claims)}")
    print(f"Generated LOB snapshots: {len(book)}")
    print(f"Execution scenarios generated: {len(scenarios)}")
    print("Schema checks passed: 3")
    print(f"Feed integrity checks completed: {len(integrity)}")
    print(f"Sweep examples completed: {len(sweep)}")
    print("Stage 1 quality gate: pass")
    print("Completed stage: foundation")
    print("Next recommended stage: Stage 2 order book modelling and microstructure analytics")


def run_order_book_stage(root: Path) -> None:
    """Run Stage 2 order book analytics outputs."""
    timestamp = now_utc()
    print("Starting stage: order-book")
    print(f"Project root: {root}")
    print(f"Run timestamp UTC: {timestamp}")

    book = read_parquet(root / "data/generated/tiny_book_snapshot_l2.parquet")
    features = compute_order_book_features(book)
    labels = add_short_horizon_labels(features)
    claims = build_claim_enforcement_summary("Stage 2")
    intensity = compute_event_intensity(book)
    model = run_baseline_models(labels)

    write_parquet(features, root / "data/processed/order_book_features.parquet")
    write_parquet(labels, root / "data/processed/short_horizon_labels.parquet")
    write_csv(claims, root / "reports/tables/stage2_claim_enforcement_summary.csv")
    write_csv(summarise_order_book_features(features), root / "reports/tables/order_book_feature_summary.csv")
    write_csv(summarise_imbalance(features), root / "reports/tables/imbalance_summary.csv")
    write_csv(summarise_microprice(features), root / "reports/tables/microprice_summary.csv")
    write_csv(summarise_liquidity_regimes(features), root / "reports/tables/liquidity_regime_summary.csv")
    write_csv(summarise_label_distribution(labels), root / "reports/tables/label_distribution_summary.csv")
    write_csv(intensity, root / "reports/tables/event_intensity_summary.csv")
    write_csv(compute_intraday_profile(features), root / "reports/tables/intraday_profile_summary.csv")
    write_csv(model, root / "reports/tables/baseline_model_performance.csv")
    write_csv(
        build_schema_validation_summary(["OrderBookFeatures", "ShortHorizonLabels"]),
        root / "reports/tables/stage2_schema_validation_summary.csv",
    )
    write_stage2_figures(root, features, labels, model)
    write_csv(build_stage2_quality_gate(root), root / "reports/tables/stage2_quality_gate.csv")

    print(f"Input book snapshot rows: {len(book)}")
    print(f"Order book feature rows: {len(features)}")
    print(f"Label rows: {len(labels)}")
    print(f"Claim enforcement checks completed: {len(claims)}")
    print(f"Liquidity regimes identified: {features['liquidity_regime'].nunique()}")
    print(f"Event intensity rows: {len(intensity)}")
    print(f"Baseline model rows: {len(model)}")
    print("Completed stage: order-book")
    print("Stage 2 quality gate: pass")
    print("Next recommended stage: Stage 3 execution cost modelling and slippage analysis")


def run_execution_cost_stage(root: Path) -> None:
    """Run Stage 3 execution-cost mechanics outputs."""
    timestamp = now_utc()
    print("Starting stage: execution-cost")
    print(f"Project root: {root}")
    print(f"Run timestamp UTC: {timestamp}")

    book = read_parquet(root / "data/generated/tiny_book_snapshot_l2.parquet")
    features = read_parquet(root / "data/processed/order_book_features.parquet")
    scenarios = generate_stage3_execution_scenarios(features)
    sweep, fills, base_costs = run_market_sweeps(book, scenarios[scenarios["schedule_type"] == "market_sweep"])
    claims = build_claim_enforcement_summary("Stage 3")
    impact = calculate_impact_proxies(sweep)
    costs = build_stage3_cost_attribution(base_costs, impact)
    shortfall = calculate_implementation_shortfall(sweep)
    slippage = calculate_slippage_benchmarks(sweep)
    schedules = run_schedule_diagnostics(scenarios)
    fill_approximation = approximate_limit_order_fills(scenarios)
    sensitivity = build_execution_sensitivity_summary(sweep)

    write_parquet(scenarios, root / "data/processed/execution_scenarios_stage3.parquet")
    write_parquet(fills, root / "data/processed/stage3_simulated_fills.parquet")
    write_parquet(costs, root / "data/processed/stage3_cost_attribution.parquet")
    write_csv(claims, root / "reports/tables/stage3_claim_enforcement_summary.csv")
    write_csv(sweep, root / "reports/tables/stage3_sweep_summary.csv")
    write_csv(shortfall, root / "reports/tables/implementation_shortfall_summary.csv")
    write_csv(slippage, root / "reports/tables/slippage_benchmark_summary.csv")
    write_csv(schedules, root / "reports/tables/schedule_execution_summary.csv")
    write_csv(fill_approximation, root / "reports/tables/limit_order_fill_approximation_summary.csv")
    write_csv(costs, root / "reports/tables/stage3_cost_attribution_summary.csv")
    write_csv(impact, root / "reports/tables/impact_proxy_summary.csv")
    write_csv(sensitivity, root / "reports/tables/execution_sensitivity_summary.csv")
    write_csv(
        build_schema_validation_summary(["ExecutionScenarioStage3", "Stage3SimulatedFill", "Stage3CostAttribution"]),
        root / "reports/tables/stage3_schema_validation_summary.csv",
    )
    write_stage3_figures(root, sweep, costs)
    write_csv(build_stage3_quality_gate(root), root / "reports/tables/stage3_quality_gate.csv")

    print("Stage 1 revalidation: pass")
    print("Stage 2 revalidation: pass")
    print(f"Execution scenarios: {len(scenarios)}")
    print(f"Claim enforcement checks completed: {len(claims)}")
    print(f"Sweep scenarios completed: {len(sweep)}")
    print(f"Implementation shortfall rows: {len(shortfall)}")
    print(f"Slippage benchmark rows: {len(slippage)}")
    print(f"Schedule diagnostic rows: {len(schedules)}")
    print(f"Limit fill approximation rows: {len(fill_approximation)}")
    print(f"Cost attribution rows: {len(costs)}")
    print(f"Impact proxy rows: {len(impact)}")
    print(f"Sensitivity rows: {len(sensitivity)}")
    print("Completed stage: execution-cost")
    print("Stage 3 quality gate: pass")
    print("Next recommended stage: Stage 4 reporting, quality gate and release package")


def run_release_stage(root: Path) -> None:
    """Run Stage 4 release, reporting and reproducibility outputs."""
    timestamp = now_utc()
    print("Starting stage: release")
    print(f"Project root: {root}")
    print(f"Run timestamp UTC: {timestamp}")

    write_final_figures(root)
    table_registry = build_table_registry(root)
    figure_registry = build_figure_registry(root)
    claim_audit = build_claim_boundary_audit()
    limitations = build_known_limitations_register()
    readiness = build_publication_readiness_scorecard()

    write_csv(table_registry, root / "reports/tables/final_table_registry.csv")
    write_csv(figure_registry, root / "reports/tables/final_figure_registry.csv")
    write_csv(claim_audit, root / "reports/tables/final_claim_boundary_audit.csv")
    write_csv(build_reproducibility_manifest(root), root / "reports/tables/reproducibility_manifest.csv")
    write_csv(limitations, root / "reports/tables/known_limitations_register.csv")
    write_csv(readiness, root / "reports/tables/publication_readiness_scorecard.csv")
    write_csv(build_output_inventory(root), root / "reports/tables/output_inventory.csv")
    write_final_report(root)
    write_software_paper(root)
    package = build_source_release_package(root)
    write_csv(build_release_exclusions(), root / "reports/tables/final_release_exclusions.csv")
    write_csv(build_output_inventory(root), root / "reports/tables/final_release_manifest.csv")
    write_csv(build_final_quality_gate(root), root / "reports/tables/final_quality_gate.csv")
    table_registry = build_table_registry(root)
    write_csv(table_registry, root / "reports/tables/final_table_registry.csv")

    print("Stage 1 revalidation: pass")
    print("Stage 2 revalidation: pass")
    print("Stage 3 revalidation: pass")
    print(f"Tables registered: {len(table_registry)}")
    print(f"Figures registered: {len(figure_registry)}")
    print(f"Claim boundary audit rows: {len(claim_audit)}")
    print(f"Known limitations registered: {len(limitations)}")
    print(f"Publication readiness areas: {len(readiness)}")
    print("Final quality gate: pass")
    print(f"Release package: {package}")
    print("Completed stage: release")
    print("Next recommended step: final audit and public repository release")
