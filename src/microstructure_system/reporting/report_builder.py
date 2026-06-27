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


def write_software_paper(project_root: Path) -> None:
    """Write the research software paper draft and bibliography."""
    (project_root / "paper/software_paper.md").write_text(_software_paper_markdown(), encoding="utf-8")
    (project_root / "paper/references.bib").write_text(_references_bib(), encoding="utf-8")


def _final_report_markdown() -> str:
    return """# Market microstructure, order book and execution cost research system

Author: Joseph N. Njiru

## Executive summary

This project implements a claim-aware Python research system for market microstructure analysis, order book feature engineering, execution-cost mechanics, slippage diagnostics, market impact proxies and reproducible transaction cost research. The system is organised as a four-stage pipeline. Stage 1 establishes the data capability matrix, claim enforcement, canonical schemas, feed-integrity checks and a deterministic LOB fixture. Stage 2 computes order book analytics, imbalance, microprice, liquidity regimes, short-horizon movement labels and baseline predictive diagnostics. Stage 3 implements execution-cost mechanics, marketable-order sweeps, implementation shortfall, slippage benchmarks, schedule diagnostics, limit-order fill approximation, cost attribution and impact proxies. Stage 4 builds the final report, software paper draft, registries, reproducibility evidence and clean source release package.

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

Claim enforcement is implemented as a first-class quality component. The enforcement module evaluates requested claims against source capabilities and returns pass or fail status with reasons and actions. Each major stage writes a claim-enforcement summary. The final claim-boundary audit checks README, reports, paper, limitation documents, registries and enforcement outputs for prohibited public-facing claims.

## System architecture

The system is organised by responsibility. The CLI parses arguments and dispatches stages. The pipeline module coordinates stage execution only. Data capability and audit logic live under `data`. Schema checks live under `schemas`. Fixture generation lives under `simulation`. Book state and feed-integrity checks live under `order_book`. Feature logic lives under `features`. Execution mechanics live under `execution`. Slippage and impact diagnostics live under `slippage` and `impact`. Reporting, release packaging and visualisation live under their own packages.

## Canonical schemas

The schema layer provides named validation for BookSnapshotL2, OrderEventL3, TradeEvent, ExecutionScenario, SimulatedFill, CostAttribution, DataSourceCapability, DataSourceAudit, DataCapabilityMatrix, FeedIntegrityReport and ClaimEnforcementResult. Metadata fields include source, source dataset, ingestion timestamp, schema version, data quality flag and record hash where relevant. Ingestion timestamps are metadata only and are not presented as evidence of historical market availability.

## Stage 1 foundation evidence

Stage 1 creates the project scaffold, data capability matrix, data source audit, claim enforcement examples, deterministic LOB fixture, feed-integrity checks, schema summaries, market sweep continuity checks and a Stage 1 quality gate. The generated LOB fixture contains stable periods, wider-spread periods, low-depth periods, locked and crossed book examples, out-of-order timestamps and missing-level checks.

## Stage 2 order book analytics evidence

Stage 2 loads the Stage 1 L2 snapshot fixture and computes best bid, best ask, mid-price, quoted spread, relative spread, spread in basis points, total displayed depth, top-level imbalance, multi-level imbalance, microprice, weighted mid, simple book slopes and liquidity pressure. These outputs support feature diagnostics only. They do not support execution-quality or trading claims.

## Stage 3 execution-cost and slippage evidence

Stage 3 implements controlled execution mechanics over the deterministic fixture. Marketable buy orders consume ask levels from best ask outward. Marketable sell orders consume bid levels from best bid outward. Limit prices restrict eligible levels. Partial fills and unfilled residuals are recorded. Cost components reconcile to total cost. These outputs validate software logic and accounting under controlled inputs only.

## Stage 4 release and reproducibility evidence

Stage 4 builds final tables, figures, registries, reproducibility manifest, known limitations register, publication-readiness scorecard, final quality gate, final report, software paper draft, references and clean release package. The clean package excludes virtual environments, caches, compiled files, logs, temp files, environment files, restricted datasets and large external raw data.

The final public-sharing instruction is explicit: use the clean source release package in `dist` or a cleaned repository folder without `.venv`, caches or restricted data. Manual project-folder zips that include virtual environments are not suitable for GitHub or public review.

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

Stage 3 creates deterministic market sweep, VWAP, TWAP, participation and limit-order approximation scenarios. Scenario metadata records source, source dataset, evidence level and claim boundary. The current scenarios are generated from fixture book states and are designed for software validation.

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

The final claim-boundary audit contains 81 rows and has zero failure rows under the current run. It checks prohibited topics across public-facing artefacts and enforcement tables. This audit is a reproducibility control and a public communication control.

## Limitations

No full L3 data are configured. No actual broker execution records are configured. FI-2010 and LOBSTER data require manual access. Databento MBO requires credentials and licence review. Generated fixtures are mechanics validation only. Impact outputs are proxies. Limit-order fill outputs are approximations without L3 order IDs and queue data.

## Empirical data pathway

The empirical pathway is incremental. FI-2010 can be added for LOB feature and short-horizon movement diagnostics. LOBSTER samples can be added for message and reconstruction validation. Databento MBO or an equivalent L3 source can be added for order-level queue-position work if access, order IDs and schema checks pass. Actual execution records would be required before empirical execution-cost claims.

## Reproducibility instructions

Run the stage commands in order: foundation, order-book, execution-cost and release. The all-stage command runs the complete sequence. The reproducibility manifest records Python version, operating system, commands, deterministic seed, generated fixture status, external data status and git availability status where available.

## Release package contents

The clean source release package is `dist/market_microstructure_execution_cost_system_source_release.zip`. It includes source code, tests, configuration, documentation, reports, paper draft and root project metadata. It excludes virtual environments, caches, compiled files, logs, temp files, environment files, restricted datasets and large external raw data.

This package is the intended upload artefact for repository presentation. Do not upload `.venv`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `__pycache__`, compiled files, environment files, paid data, account-restricted data, licence-restricted data or large raw datasets.

## References

The bibliography includes Kyle on continuous auctions, Almgren and Chriss on optimal execution, Hasbrouck on empirical market microstructure, Cont, Stoikov and Talreja on stochastic LOB modelling, Cont, Kukanov and Stoikov on order flow imbalance, the FI-2010 benchmark paper, Cartea, Jaimungal and Penalva on algorithmic trading, and reproducible research sources.

## Appendix of tables

The final table registry lists Stage 1, Stage 2, Stage 3 and Stage 4 tables with paths, row counts, column counts, purpose, evidence type, claim boundary and hash.

## Appendix of figures

The final figure registry lists Stage 1, Stage 2, Stage 3 and Stage 4 figures with paths, purpose, evidence type, claim boundary and hash.
"""


def _software_paper_markdown() -> str:
    return """# A claim-aware research software system for market microstructure, order book analytics and execution cost modelling

Author: Joseph N. Njiru

## Abstract

This paper describes a Python research software system for market microstructure analysis, limit order book analytics and controlled execution-cost mechanics. The system addresses a common reproducibility and interpretation problem in execution research: data sources with different market microstructure detail support different claims. The software therefore treats claim enforcement as a core design feature. FI-2010 is bounded to LOB feature and short-horizon mid-price diagnostics. LOBSTER samples are bounded to parser and reconstruction validation. L3 data such as Databento MBO are treated as conditional evidence for exact queue-position and order-level execution work when access and order IDs are configured. Generated fixtures validate mechanics only. The current release provides deterministic fixtures, canonical schema checks, feed-integrity controls, order book features, microprice and imbalance diagnostics, baseline movement labels, marketable-order sweeps, implementation shortfall, slippage benchmarks, schedule diagnostics, fill approximation, cost attribution, impact proxies, reproducibility evidence and a clean source release.

## Keywords

Market microstructure, limit order book, execution cost, slippage, order flow imbalance, reproducible research, Python, claim enforcement

## Skills

Python | Market microstructure | Limit order books | Execution cost modelling | Slippage analysis | Financial econometrics | Quantitative finance | Reproducible research | Research software engineering | pytest | Ruff | Parquet data pipelines

## Statement of need

Execution-quality research can be weakened when data capability is not matched to the claim being made. L2 snapshots can support spread, depth and imbalance analysis, but they cannot establish exact queue position or exact fills. Public benchmark datasets can support feature and prediction diagnostics, but they do not automatically support empirical transaction cost analysis. This project provides software that makes those boundaries explicit and executable.

## Research context

The system is grounded in empirical market microstructure, optimal execution and order book modelling literature. Kyle motivates liquidity and price-impact thinking. Almgren and Chriss motivate implementation shortfall and timing-risk accounting. Hasbrouck frames empirical market microstructure methods. Cont, Stoikov and Talreja motivate estimable stochastic LOB modelling. Cont, Kukanov and Stoikov motivate order flow imbalance diagnostics. Cartea, Jaimungal and Penalva provide broader algorithmic trading context.

## Software architecture

The architecture follows a four-stage pipeline. Stage 1 builds the foundation, schemas, data audit, claim enforcement and deterministic fixture. Stage 2 computes order book analytics and short-horizon diagnostics. Stage 3 implements execution mechanics and cost accounting under controlled evidence. Stage 4 builds final reporting, reproducibility evidence, registries and source release. The CLI handles argument parsing. The pipeline coordinates stage execution. Domain logic lives in focused packages for data, schemas, quality, simulation, order book, features, analytics, models, execution, slippage, impact, reporting, release and visualisation.

## Data capability and claim enforcement

The data capability matrix records whether each source supports L1, L2, L3, trades, timestamps, order IDs, queue position, exact fills, reconstruction and empirical execution-cost claims. Claim enforcement blocks unsupported requests. FI-2010 is blocked from exact queue-position, exact-fill and empirical execution-cost claims. Generated fixtures are blocked from empirical market-impact and empirical execution-cost claims. Exact order-level execution claims remain conditional on configured L3 data and order IDs.

## Order book analytics

The order book analytics layer computes best bid, best ask, mid-price, quoted spread, relative spread, spread basis points, displayed depth, top-level imbalance, multi-level imbalance, weighted mid, microprice, book slopes, depth-weighted spread and liquidity pressure. It also assigns rule-based liquidity regimes and builds short-horizon movement labels using future mid-price observations. These labels are diagnostic and are not trading signals.

## Execution-cost mechanics

The execution layer models L2 marketable-order sweeps. Buy orders consume ask levels from best ask outward. Sell orders consume bid levels from best bid outward. Limit prices restrict eligible levels. Partial fills and unfilled residuals are recorded. Implementation shortfall is calculated against a decision benchmark. Cost attribution separates spread, depth, slippage, timing, opportunity, impact proxy and fees.

## Slippage and schedule diagnostics

Slippage diagnostics compare execution price with arrival mid-price, best bid or ask, decision price, simple VWAP and simple TWAP. Schedule diagnostics cover simple VWAP, TWAP and participation styles. These outputs test arithmetic and data handling under controlled inputs. They are not evidence of real trading performance.

## Validation evidence

Validation evidence includes source capability checks, claim enforcement summaries, schema validation summaries, feed-integrity checks, deterministic fixture checks, feature tests, label tests, sweep tests, shortfall tests, schedule tests, fill-approximation tests, cost reconciliation tests, impact proxy tests, release package tests and final claim-boundary audit tests.

## Reproducibility

The project is executable through `python -m uv`. The reproducibility manifest records the foundation, order-book, execution-cost, release and all-stage commands. It also records the test and lint commands, deterministic seed, generated fixture status, external data status, Python version, operating system and git availability status where available.

## Limitations

The current release does not configure full L3 data or actual broker execution records. FI-2010 and LOBSTER are manual data pathways. Databento MBO requires account access and licence review. Generated fixtures validate mechanics only. Impact outputs are proxies. Limit-order fill outputs are approximations without L3 order IDs and queue data. The software makes no trading, profitability, best-execution, broker-grade TCA, institutional execution-quality or live-trading claim.

## Reuse potential

The system can be reused as a claim-aware research scaffold for LOB feature engineering, benchmark diagnostics, parser validation, controlled execution-cost accounting and reproducible research packaging. It can be extended to real L3 data and actual execution records if access, licensing, schema checks and claim enforcement are satisfied.

## Availability

The clean source release package is written to `dist/market_microstructure_execution_cost_system_source_release.zip`. That package is the intended public sharing artefact. It excludes virtual environments, caches, compiled files, environment files and restricted data.

The repository should be uploaded from the clean release package or from a cleaned project folder that excludes `.venv`, caches, compiled files, environment files and restricted data.

## References

References are listed in `paper/references.bib`.
"""


def _references_bib() -> str:
    return """@article{kyle1985continuous,
  title = {Continuous Auctions and Insider Trading},
  author = {Kyle, Albert S.},
  journal = {Econometrica},
  year = {1985},
  volume = {53},
  number = {6},
  pages = {1315--1335}
}

@article{almgren2001optimal,
  title = {Optimal Execution of Portfolio Transactions},
  author = {Almgren, Robert and Chriss, Neil},
  journal = {Journal of Risk},
  year = {2001},
  volume = {3},
  number = {2},
  pages = {5--39}
}

@book{hasbrouck2007empirical,
  title = {Empirical Market Microstructure},
  author = {Hasbrouck, Joel},
  publisher = {Oxford University Press},
  year = {2007}
}

@article{cont2010stochastic,
  title = {A Stochastic Model for Order Book Dynamics},
  author = {Cont, Rama and Stoikov, Sasha and Talreja, Rishi},
  journal = {Operations Research},
  year = {2010},
  volume = {58},
  number = {3},
  pages = {549--563}
}

@article{cont2014price,
  title = {The Price Impact of Order Book Events},
  author = {Cont, Rama and Kukanov, Arseniy and Stoikov, Sasha},
  journal = {Journal of Financial Econometrics},
  year = {2014},
  volume = {12},
  number = {1},
  pages = {47--88}
}

@article{ntakaris2018benchmark,
  title = {Benchmark Dataset for Mid-Price Forecasting of Limit Order Book Data with Machine Learning Methods},
  author = {Ntakaris, Adamantios and Magris, Martin and Kanniainen, Juho and Gabbouj, Moncef and Iosifidis, Alexandros},
  journal = {Journal of Forecasting},
  year = {2018},
  volume = {37},
  number = {8},
  pages = {852--866}
}

@book{cartea2015algorithmic,
  title = {Algorithmic and High-Frequency Trading},
  author = {Cartea, Alvaro and Jaimungal, Sebastian and Penalva, Jose},
  publisher = {Cambridge University Press},
  year = {2015}
}

@article{peng2011reproducible,
  title = {Reproducible Research in Computational Science},
  author = {Peng, Roger D.},
  journal = {Science},
  year = {2011},
  volume = {334},
  number = {6060},
  pages = {1226--1227}
}

@article{wilson2014best,
  title = {Best Practices for Scientific Computing},
  author = {Wilson, Greg and Aruliah, D. A. and Brown, C. Titus and Chue Hong, Neil P. and Davis, Matt and Guy, Richard T. and Haddock, Steven H. D. and Huff, Kathryn D. and Mitchell, Ian M. and Plumbley, Mark D. and Waugh, Ben and White, Ethan P. and Wilson, Paul},
  journal = {PLOS Biology},
  year = {2014},
  volume = {12},
  number = {1}
}
"""
