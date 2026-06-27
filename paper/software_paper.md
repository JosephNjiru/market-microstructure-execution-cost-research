# A claim-aware research software system for market microstructure, order book analytics and execution cost modelling

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
