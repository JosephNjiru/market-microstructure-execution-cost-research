from __future__ import annotations

from pathlib import Path


def write_final_report(project_root: Path) -> None:
    """Write the final Markdown and HTML reports."""
    report = _final_report_markdown()
    (project_root / "reports/market_microstructure_execution_cost_report.md").write_text(
        report,
        encoding="utf-8",
    )
    html = "<html><body>" + report.replace("\n", "<br>") + "</body></html>"
    (project_root / "reports/market_microstructure_execution_cost_report.html").write_text(
        html,
        encoding="utf-8",
    )


def _final_report_markdown() -> str:
    return """# Market microstructure, order book and execution cost research system

Author: Joseph N. Njiru

## Executive summary

This project implements a claim-aware Python research system for market microstructure analysis, order book feature engineering, execution-cost mechanics, slippage diagnostics, market impact proxies and reproducible transaction cost research. The system is organised as a four-stage pipeline. The foundation stage establishes the data capability matrix, claim enforcement, canonical schemas, feed-integrity checks and a deterministic LOB fixture. The order book stage computes analytics, imbalance, microprice, liquidity regimes, short-horizon movement labels and baseline predictive diagnostics. The execution-cost stage implements marketable-order sweeps, implementation shortfall, slippage benchmarks, schedule diagnostics, limit-order fill approximation, cost attribution and impact proxies. The release stage builds the final report, registries, reproducibility evidence and quality-gate artefacts.

The project is deliberately conservative. Generated data validate mechanics and accounting only. FI-2010 is treated as a public LOB feature and mid-price movement benchmark, not as execution-cost evidence. LOBSTER samples are treated as parser and reconstruction validation where available. Databento MBO or equivalent L3 data remains the conditional route for exact queue-position and order-level execution claims. No trading, profitability, best-execution, broker-grade TCA, institutional execution-quality or live-trading claim is made.

## Skills demonstrated

Python | Market microstructure | Limit order books | Execution cost modelling | Slippage analysis | Financial econometrics | Quantitative finance | Reproducible research | Research software engineering | pytest | Ruff | Parquet data pipelines

## Research aim

The aim is to provide an auditable research software foundation for studying how displayed order book state, queue depth, liquidity regime and order flow diagnostics relate to short-horizon price movement and execution-cost mechanics. The project separates empirical benchmark diagnostics from controlled mechanics validation. This separation is essential because execution quality cannot be inferred from prices alone.

## Evidence boundary

The evidence boundary is enforced in code, configuration, tests and final artefacts. FI-2010 supports LOB features, spread, depth, imbalance and short-horizon mid-price movement diagnostics only. LOBSTER samples support parser and reconstruction checks only where files are present. Databento MBO or equivalent L3 data may support exact queue-position and order-level execution claims only if credentials, order IDs and schema checks are configured. Binance public data is secondary ingestion evidence unless audited historical depth-event files are confirmed. Controlled generated fixtures support mechanics validation, stress checks and accounting reconciliation only.

## Data capability matrix

The data capability matrix records source-level support for L1, L2, L3, trades, timestamps, order IDs, queue position, exact fills, reconstruction and empirical execution-cost claims. The current public configuration includes five source rows: FI-2010, LOBSTER_sample, Databento_MBO_optional, Binance_public_data_secondary and controlled_calibrated_simulation. The matrix blocks FI-2010, generated fixtures and secondary public data from exact fill, exact queue-position and empirical execution-cost claims.

## Claim enforcement design

Claim enforcement is implemented as a first-class quality component. The enforcement module evaluates requested claims against source capabilities and returns pass or fail status with reasons and actions. Each major stage writes a claim-enforcement summary. The final claim-boundary audit checks README, reports, limitation documents, registries and enforcement outputs for prohibited public-facing claims.

## System architecture

The system is organised by responsibility. The CLI parses arguments and dispatches stages. The pipeline module coordinates stage execution only. Data capability and audit logic live under `data`. Schema checks live under `schemas`. Fixture generation lives under `simulation`. Book state and feed-integrity checks live under `order_book`. Feature logic lives under `features`. Execution mechanics live under `execution`. Slippage and impact diagnostics live under `slippage` and `impact`. Reporting, release packaging and visualisation live under their own packages.

## Canonical schemas

The schema layer provides named validation for BookSnapshotL2, OrderEventL3, TradeEvent, ExecutionScenario, SimulatedFill, CostAttribution, DataSourceCapability, DataSourceAudit, DataCapabilityMatrix, FeedIntegrityReport and ClaimEnforcementResult. Metadata fields include source, source dataset, ingestion timestamp, schema version, data quality flag and record hash where relevant. Ingestion timestamps are metadata only and are not presented as evidence of historical market availability.

## Foundation evidence

The foundation layer creates the project scaffold, data capability matrix, data source audit, claim enforcement examples, deterministic LOB fixture, feed-integrity checks, schema summaries, market sweep continuity checks and a quality gate. The generated LOB fixture contains stable periods, wider-spread periods, low-depth periods, locked and crossed book examples, out-of-order timestamps and missing-level checks.

## Order book analytics evidence

The order book analytics layer loads the L2 snapshot fixture and computes best bid, best ask, mid-price, quoted spread, relative spread, spread in basis points, total displayed depth, top-level imbalance, multi-level imbalance, microprice, weighted mid, simple book slopes and liquidity pressure. These outputs support feature diagnostics only. They do not support execution-quality or trading claims.

## Execution-cost and slippage evidence

The execution-cost layer implements controlled execution mechanics over the deterministic fixture. Marketable buy orders consume ask levels from best ask outward. Marketable sell orders consume bid levels from best bid outward. Limit prices restrict eligible levels. Partial fills and unfilled residuals are recorded. Cost components reconcile to total cost. These outputs validate software logic and accounting under controlled inputs only.

## Release and reproducibility evidence

The release layer builds final tables, figures, registries, reproducibility manifest, known limitations register, publication-readiness scorecard, final quality gate and final report. Redistribution controls exclude virtual environments, caches, compiled files, logs, temp files, environment files, restricted datasets and large external raw data.

## Order book feature summary

The feature summary table reports descriptive statistics for mid-price, quoted spread, spread basis points, total depth, top-level imbalance, multi-level imbalance and microprice displacement. These values come from the controlled fixture unless eligible real data are configured. The table is useful for checking that the analytics layer behaves consistently across valid and invalid book states.

## Imbalance and microprice summary

Top-level imbalance uses displayed quantity at the best bid and best ask. Multi-level imbalance uses cumulative depth across displayed levels. Microprice weights the best bid and best ask by opposing displayed size. The fixture includes balanced and low-depth states so the diagnostics can test denominator handling and signal labelling.

## Liquidity regime summary

Stage 2 assigns rule-based regimes: normal, wide_spread, low_depth, wide_spread_low_depth and invalid. The current fixture produces normal, wide-spread and invalid states. The invalid states correspond to locked, crossed or incomplete books and are used to test quality controls.

## Short-horizon diagnostic labels

Short-horizon labels use future mid-price observations at one, three, five and ten event horizons. Boundary rows without sufficient future observations are flagged. The labels are predictive diagnostics only. They are not trading signals and are not evidence of execution performance.

## Baseline model diagnostics

Baseline diagnostics include a naive majority-class model and a transparent logistic-regression placeholder under controlled fixture evidence. The model evidence level is controlled_fixture_diagnostic. If FI-2010 is manually configured, the allowed claim level remains a public LOB benchmark diagnostic, not an execution-cost claim.

## Execution scenarios

The execution-cost layer creates deterministic market sweep, VWAP, TWAP, participation and limit-order approximation scenarios. Scenario metadata records source, source dataset, evidence level and claim boundary. The current scenarios are generated from fixture book states and are designed for software validation.

## Marketable-order sweep results

The sweep summary records filled quantity, unfilled quantity, quantity-weighted average price, arrival mid-price, spread, consumed levels, gross notional, execution status and cost basis points. Larger orders consume deeper levels under the same book state. Partial fills and unfilled residuals are explicit.

## Implementation shortfall

Implementation shortfall is calculated against the decision price at the order timestamp. For buys, adverse shortfall is execution price above decision price. For sells, adverse shortfall is execution price below decision price. Partial fills include an opportunity-cost assumption for unfilled quantity. This is a mechanics assumption, not empirical evidence.

## Slippage benchmarks

Slippage diagnostics compare execution price with arrival mid-price, best bid or ask, decision price, simple VWAP and simple TWAP benchmarks. The sign convention is adverse-cost oriented. Benchmark outputs are diagnostic and do not imply execution quality under real venue conditions.

## Schedule diagnostics

VWAP, TWAP and participation diagnostics split target quantity across available controlled fixture timestamps. The schedule tables record target quantity, filled quantity, unfilled quantity, mean slice price, quantity-weighted average price, benchmark price and schedule status. These diagnostics validate scheduling arithmetic only.

## Limit-order fill approximation

Limit-order fill logic is labelled as approximation. Without L3 order IDs and queue position, the system cannot claim exact fills. The output records approximate filled quantity, approximate unfilled quantity, approximation status and a flag that exact claims require L3 data.

## Cost attribution reconciliation

Cost attribution separates spread cost, depth cost, slippage cost, timing cost, opportunity cost, impact proxy cost and fees. Fees are recorded as zero when no fee schedule is configured. The reconciliation check verifies that the components sum to total cost within floating-point tolerance.

## Impact proxies

Impact outputs are labelled as proxies. The system reports cost by order-size bucket, cost by liquidity regime, marginal depth cost and post-trade mid-price movement where available. Fixture-based post-trade movement does not prove real market impact.

## Sensitivity analysis

Sensitivity outputs summarise deterministic changes across order-size bucket, spread regime and fee assumption. The table records mean, median and maximum cost basis points, partial-fill counts and unfilled counts. The purpose is to test mechanics and accounting under controlled variation.

## Final claim-boundary audit

The final claim-boundary audit records the current run checks and has zero failure rows under the current configuration. It checks prohibited topics across public-facing artefacts and enforcement tables. This audit is a reproducibility control and a public communication control.

## Limitations

No full L3 data are configured. No actual broker execution records are configured. FI-2010 and LOBSTER data require manual access. Databento MBO requires credentials and licence review. Generated fixtures are mechanics validation only. Impact outputs are proxies. Limit-order fill outputs are approximations without L3 order IDs and queue data.

## Empirical data pathway

The empirical pathway is incremental. FI-2010 can be added for LOB feature and short-horizon movement diagnostics. LOBSTER samples can be added for message and reconstruction validation. Databento MBO or an equivalent L3 source can be added for order-level queue-position work if access, order IDs and schema checks pass. Actual execution records would be required before empirical execution-cost claims.

## Reproducibility instructions

Run the stage commands in order: foundation, order-book, execution-cost and release. The all-stage command runs the complete sequence. The reproducibility manifest records Python version, operating system, commands, deterministic seed, generated fixture status, external data status and git availability status where available.

## Release package contents

The release manifest records source code, tests, configuration, documentation, reports and root project metadata. Redistribution controls exclude virtual environments, caches, compiled files, logs, temp files, environment files, restricted datasets and large external raw data.

## References

The research basis includes Kyle on continuous auctions, Almgren and Chriss on optimal execution, Hasbrouck on empirical market microstructure, Cont, Stoikov and Talreja on stochastic LOB modelling, Cont, Kukanov and Stoikov on order flow imbalance, the FI-2010 benchmark paper, Cartea, Jaimungal and Penalva on algorithmic trading, and reproducible research sources.

## Appendix of tables

The final table registry lists evidence tables with paths, row counts, column counts, purpose, evidence type, claim boundary and hash.

## Appendix of figures

The final figure registry lists evidence figures with paths, purpose, evidence type, claim boundary and hash.
"""
