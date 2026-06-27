from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from microstructure_system.analytics.execution_summary import summarise_execution_outputs
from microstructure_system.analytics.intraday_profiles import compute_intraday_profile
from microstructure_system.analytics.liquidity_regimes import summarise_liquidity_regimes
from microstructure_system.analytics.order_book_summary import summarise_order_book_features
from microstructure_system.data.source_audit import (
    build_data_capability_matrix,
    run_data_source_audit,
)
from microstructure_system.execution.cost_attribution import components_reconcile
from microstructure_system.execution.fill_model import approximate_limit_order_fills
from microstructure_system.execution.implementation_shortfall import (
    calculate_implementation_shortfall,
)
from microstructure_system.execution.market_sweep import run_market_sweeps
from microstructure_system.execution.scenarios import generate_stage3_execution_scenarios
from microstructure_system.execution.schedule import run_schedule_diagnostics
from microstructure_system.features.book_features import compute_order_book_features
from microstructure_system.features.event_intensity import compute_event_intensity
from microstructure_system.features.imbalance import top_level_imbalance
from microstructure_system.features.labels import add_short_horizon_labels
from microstructure_system.features.liquidity import classify_liquidity_regime
from microstructure_system.features.microprice import calculate_microprice
from microstructure_system.impact.market_impact import calculate_impact_proxies
from microstructure_system.impact.sensitivity import build_execution_sensitivity_summary
from microstructure_system.models.baselines import run_baseline_models
from microstructure_system.models.evaluation import accuracy
from microstructure_system.order_book.book_state import best_ask, best_bid, mid_price
from microstructure_system.order_book.integrity import run_feed_integrity_checks
from microstructure_system.quality.claim_enforcement import enforce_claim_boundary
from microstructure_system.quality.final_quality import build_final_quality_gate
from microstructure_system.quality.stage1_quality import build_stage1_quality_gate
from microstructure_system.quality.stage2_quality import build_stage2_quality_gate
from microstructure_system.quality.stage3_quality import build_stage3_quality_gate
from microstructure_system.release.manifest import (
    build_output_inventory,
    build_release_exclusions,
)
from microstructure_system.release.reproducibility import build_reproducibility_manifest
from microstructure_system.reporting.claim_boundary_audit import build_claim_boundary_audit
from microstructure_system.reporting.figure_registry import build_figure_registry
from microstructure_system.reporting.publication_readiness import (
    build_known_limitations_register,
    build_publication_readiness_scorecard,
)
from microstructure_system.reporting.table_registry import build_table_registry
from microstructure_system.schemas.validation import validate_named_frame
from microstructure_system.simulation.lob_fixture import generate_tiny_lob_fixture
from microstructure_system.slippage.analysis import calculate_slippage_benchmarks
from microstructure_system.slippage.benchmarks import adverse_slippage
from microstructure_system.utils.hashing import add_record_hashes

ROOT = Path.cwd()


def _book() -> pd.DataFrame:
    return generate_tiny_lob_fixture()


def _features() -> pd.DataFrame:
    return compute_order_book_features(_book())


def _scenarios() -> pd.DataFrame:
    return generate_stage3_execution_scenarios(_features())


def _sweeps() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scenarios = _scenarios()
    return run_market_sweeps(_book(), scenarios[scenarios["schedule_type"] == "market_sweep"])


def test_data_capability_matrix_restores_required_sources_and_boundaries() -> None:
    matrix = build_data_capability_matrix()
    assert {
        "FI-2010",
        "LOBSTER_sample",
        "Databento_MBO_optional",
        "Binance_public_data_secondary",
        "controlled_calibrated_simulation",
    }.issubset(set(matrix["source_name"]))
    fi = matrix[matrix["source_name"] == "FI-2010"].iloc[0]
    assert not bool(fi["supports_queue_position"])
    assert not bool(fi["supports_exact_fills"])
    assert not bool(fi["supports_empirical_execution_cost_claims"])
    sim = matrix[matrix["source_name"] == "controlled_calibrated_simulation"].iloc[0]
    assert sim["allowed_claim_level"] == "controlled_mechanics_validation"


def test_data_source_audit_records_manual_and_conditional_access() -> None:
    audit = run_data_source_audit()
    assert "requires_manual_download" in set(audit["access_status"])
    assert "requires_account" in set(audit["access_status"])
    assert audit.loc[audit["source_name"] == "controlled_calibrated_simulation", "download_success"].iloc[0]


def test_claim_enforcement_blocks_execution_claims_from_weak_sources() -> None:
    assert enforce_claim_boundary("FI-2010", "exact_queue_position").enforcement_status == "fail"
    assert enforce_claim_boundary("FI-2010", "empirical_execution_cost").enforcement_status == "fail"
    assert (
        enforce_claim_boundary("controlled_calibrated_simulation", "empirical_market_impact").enforcement_status
        == "fail"
    )
    assert (
        enforce_claim_boundary("controlled_calibrated_simulation", "controlled_mechanics_validation").enforcement_status
        == "pass"
    )


def test_canonical_schema_validation_accepts_known_names() -> None:
    result = validate_named_frame("BookSnapshotL2", _book())
    assert result["status"] == "pass"
    assert validate_named_frame("UnknownSchema", _book())["status"] == "fail"


def test_generated_lob_fixture_is_deterministic() -> None:
    pd.testing.assert_frame_equal(_book(), _book())


def test_book_state_calculates_best_prices_and_mid() -> None:
    snapshot = _book().iloc[0]
    assert best_bid(snapshot) < best_ask(snapshot)
    assert mid_price(snapshot) == (best_bid(snapshot) + best_ask(snapshot)) / 2


def test_feed_integrity_detects_crossed_locked_missing_and_out_of_order_rows() -> None:
    checks = run_feed_integrity_checks(_book()).set_index("check_name")
    assert checks.loc["crossed_book_detection", "invalid_count"] >= 1
    assert checks.loc["locked_book_detection", "invalid_count"] >= 1
    assert checks.loc["missing_level_detection", "invalid_count"] >= 1
    assert checks.loc["out_of_order_timestamp_detection", "invalid_count"] >= 1


def test_order_book_features_calculate_core_l1_l2_measures() -> None:
    features = _features()
    row = features.iloc[0]
    assert row["mid_price"] == (row["best_bid_price"] + row["best_ask_price"]) / 2
    assert row["quoted_spread"] == row["best_ask_price"] - row["best_bid_price"]
    assert "liquidity_pressure_score" in features.columns


def test_imbalance_handles_regular_and_zero_depth_cases() -> None:
    assert top_level_imbalance(600, 400) == 0.2
    assert top_level_imbalance(0, 0) is None


def test_microprice_formula_and_direction() -> None:
    price = calculate_microprice(100.02, 100.00, 800, 200)
    assert price > 100.01


def test_liquidity_regime_classification() -> None:
    assert classify_liquidity_regime(False, 1.0) == "invalid"
    assert classify_liquidity_regime(True, 5.0) == "wide_spread"
    assert classify_liquidity_regime(True, 1.0) == "normal"


def test_labels_use_future_observations_and_flag_boundaries() -> None:
    labels = add_short_horizon_labels(_features())
    assert labels.loc[0, "future_mid_price_1_event"] == _features().loc[1, "mid_price"]
    assert labels["label_boundary_flag_10_event"].sum() == 10


def test_event_intensity_records_duplicate_and_ordering_flags() -> None:
    intensity = compute_event_intensity(_book())
    assert "low_activity_period_flag" in intensity.columns
    assert intensity["out_of_order_timestamp_count"].iloc[0] >= 1


def test_intraday_profile_is_limited_for_tiny_fixture() -> None:
    profile = compute_intraday_profile(_features())
    assert profile["profile_status"].iloc[0] == "limited_fixture"


def test_baseline_models_and_evaluation_are_diagnostic_only() -> None:
    labels = add_short_horizon_labels(_features())
    model = run_baseline_models(labels)
    assert set(model["model_evidence_level"]) == {"controlled_fixture_diagnostic"}
    assert accuracy(pd.Series(["up", "down"]), pd.Series(["up", "flat"])) == 0.5


def test_execution_scenarios_include_required_stage3_types() -> None:
    scenarios = _scenarios()
    assert {"market_sweep", "vwap", "twap", "participation", "limit_order"}.issubset(
        set(scenarios["schedule_type"])
    )
    assert set(scenarios["evidence_level"]) == {"controlled_mechanics_validation"}


def test_market_sweep_consumes_correct_sides_and_records_levels() -> None:
    sweep, fills, _ = _sweeps()
    buy = fills[fills["side"] == "buy"]
    sell = fills[fills["side"] == "sell"]
    assert buy["price"].min() >= _book()["ask_price_1"].min()
    assert sell["price"].max() <= _book()["bid_price_1"].max()
    assert sweep["levels_consumed"].max() >= 2


def test_larger_market_sweeps_have_equal_or_higher_cost() -> None:
    sweep, _, _ = _sweeps()
    small = sweep.loc[sweep["scenario_id"] == "market_sweep_small", "total_cost"].iloc[0]
    large = sweep.loc[sweep["scenario_id"] == "market_sweep_large", "total_cost"].iloc[0]
    assert large >= small


def test_partial_fills_and_unfilled_residuals_are_recorded() -> None:
    sweep, _, _ = _sweeps()
    assert (sweep["unfilled_quantity"] > 0).any()
    assert set(sweep["execution_status"]).issubset({"filled", "partial_fill"})


def test_cost_attribution_components_reconcile() -> None:
    _, _, costs = _sweeps()
    assert costs.apply(components_reconcile, axis=1).all()


def test_implementation_shortfall_uses_adverse_cost_convention() -> None:
    sweep, _, _ = _sweeps()
    shortfall = calculate_implementation_shortfall(sweep)
    assert (shortfall["implementation_shortfall"] >= 0).all()
    assert (shortfall["implementation_shortfall_bps"] >= 0).all()


def test_slippage_benchmarks_use_side_aware_signs() -> None:
    assert adverse_slippage("buy", 101, 100) == 1
    assert adverse_slippage("sell", 99, 100) == 1
    sweep, _, _ = _sweeps()
    slippage = calculate_slippage_benchmarks(sweep)
    assert {"arrival_mid_price", "simple_vwap", "simple_twap"}.issubset(set(slippage["benchmark_type"]))


def test_schedule_diagnostics_reconcile_quantities() -> None:
    schedules = run_schedule_diagnostics(_scenarios())
    assert (schedules["filled_quantity"] + schedules["unfilled_quantity"]).equals(
        schedules["target_quantity"]
    )


def test_limit_fill_approximation_requires_l3_for_exact_claims() -> None:
    fills = approximate_limit_order_fills(_scenarios())
    assert fills["requires_l3_for_exact_claim"].all()
    assert fills["approx_fill_status"].str.contains("approximation").all()


def test_impact_proxy_is_labelled_as_proxy() -> None:
    sweep, _, _ = _sweeps()
    impact = calculate_impact_proxies(sweep)
    assert impact["claim_boundary"].str.contains("Impact proxy").all()


def test_sensitivity_summary_is_deterministic() -> None:
    sweep, _, _ = _sweeps()
    first = build_execution_sensitivity_summary(sweep)
    second = build_execution_sensitivity_summary(sweep)
    pd.testing.assert_frame_equal(first, second)


def test_order_book_and_execution_summaries_are_non_empty() -> None:
    sweep, _, _ = _sweeps()
    assert not summarise_order_book_features(_features()).empty
    assert not summarise_liquidity_regimes(_features()).empty
    assert not summarise_execution_outputs(sweep).empty


def test_quality_gate_builders_return_pass_rows() -> None:
    for builder in [
        build_stage1_quality_gate,
        build_stage2_quality_gate,
        build_stage3_quality_gate,
        build_final_quality_gate,
    ]:
        gate = builder(ROOT)
        assert not gate.empty
        assert set(gate["status"]) == {"pass"}


def test_final_reporting_registries_and_claim_audit() -> None:
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(
        set(build_table_registry(ROOT)["stage"])
    )
    assert {"Stage 1", "Stage 2", "Stage 3", "Stage 4"}.issubset(
        set(build_figure_registry(ROOT)["stage"])
    )
    assert not (build_claim_boundary_audit()["claim_status"] == "fail").any()


def test_reproducibility_and_publication_readiness_modules() -> None:
    repro = build_reproducibility_manifest(ROOT)
    limitations = build_known_limitations_register()
    readiness = build_publication_readiness_scorecard()
    assert "all stages command" in set(repro["item"])
    assert len(limitations) >= 11
    assert "release package" in set(readiness["area"])


def test_release_inventory_and_exclusions_modules() -> None:
    inventory = build_output_inventory(ROOT)
    exclusions = build_release_exclusions()
    assert not inventory.empty
    assert {".venv", "__pycache__"}.issubset(set(exclusions["pattern"]))


def test_release_package_contains_modular_source_layout() -> None:
    package = ROOT / "dist/market_microstructure_execution_cost_system_source_release.zip"
    assert package.exists()
    with ZipFile(package) as archive:
        names = set(archive.namelist())
    required = {
        "src/microstructure_system/pipeline.py",
        "src/microstructure_system/features/book_features.py",
        "src/microstructure_system/execution/market_sweep.py",
        "src/microstructure_system/reporting/report_builder.py",
        "src/microstructure_system/release/source_package.py",
    }
    assert required.issubset(names)


def test_record_hash_utility_adds_hash_column() -> None:
    hashed = add_record_hashes(pd.DataFrame({"a": [1], "b": [2]}))
    assert "record_hash" in hashed.columns
    assert len(hashed["record_hash"].iloc[0]) == 64
