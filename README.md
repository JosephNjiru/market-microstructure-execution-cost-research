# Market microstructure execution cost research

Author: Joseph N. Njiru

This repository contains a claim-aware Python research system for market microstructure, order book analytics, execution-cost mechanics, slippage diagnostics, impact proxies and reproducible transaction cost research.

The system is designed for technical review by quantitative finance practitioners, market microstructure researchers, research software engineers and reproducibility reviewers. It emphasises data capability boundaries, executable claim checks, deterministic fixtures, canonical schemas and auditable outputs.

## Evidence boundary

Generated fixtures are used for mechanics validation and accounting checks only. They are not empirical market evidence. FI-2010 is treated as a public LOB benchmark for features and short-horizon mid-price movement only. Exact queue-position, exact-fill and empirical execution-cost claims require suitable L3 order-level data with order IDs and appropriate access.

The project does not claim trading readiness, profitability, best-execution compliance, broker-grade transaction-cost analysis, institutional-grade execution evidence, live-trading readiness, empirical execution cost from generated or L2 data, or empirical market impact from generated fixtures.

## Key capabilities

- Data capability matrix for public benchmarks, sample order book files, conditional L3 data, secondary public market data and generated fixtures.
- Executable claim enforcement for source-specific evidence boundaries.
- Canonical schemas for book snapshots, events, execution scenarios, simulated fills, cost attribution, source audit outputs and quality reports.
- Deterministic generated LOB fixtures for feed integrity, sweep mechanics and accounting checks.
- Order book feature engineering, including spread, depth, imbalance, microprice, liquidity regimes and event intensity summaries.
- Short-horizon mid-price movement labels for diagnostic modelling only.
- Transparent baseline models for feature diagnostics, with conservative evidence labelling.
- Marketable-order sweep mechanics, implementation shortfall accounting, slippage benchmarks and schedule diagnostics.
- Limit-order fill approximation with explicit L3 requirements for exact-fill claims.
- Cost attribution, reconciliation checks, impact proxies and sensitivity summaries.
- Reproducibility outputs, quality gates, claim-boundary audit tables and technical reports.

## Repository structure

```text
config/                     Configuration and claim policy files
data/generated/             Deterministic generated fixtures
data/processed/             Pipeline outputs created from permitted inputs
docs/                       Methodology, limitations and data governance notes
reports/                    Public technical reports, tables and figures
src/microstructure_system/  Python package source
tests/                      pytest suite
run_project.py              Pipeline entry point
pyproject.toml              Project metadata and tooling configuration
```

The GitHub repository excludes local distribution folders, virtual environments, caches and separate publication materials.

## Setup

Install Python 3.11 and `uv`, then create the project environment from the repository root.

```powershell
python -m uv sync
```

If `uv` is installed as a direct command, the equivalent `uv sync` command is also suitable.

## Run the pipeline

Run each pipeline section explicitly:

```powershell
python -m uv run python run_project.py --stage foundation
python -m uv run python run_project.py --stage order-book
python -m uv run python run_project.py --stage execution-cost
python -m uv run python run_project.py --stage release
```

Run the complete pipeline:

```powershell
python -m uv run python run_project.py --stage all --config config/project_config.yaml
```

## Validation

Run the local validation suite:

```powershell
python -m uv run pytest
python -m uv run ruff check .
```

The GitHub Actions workflow runs the same test and lint checks on push and pull request.

## Data-source boundaries

| Source | Role in this project | Boundary |
| --- | --- | --- |
| FI-2010 | Public LOB benchmark for features and short-horizon mid-price movement | Not sufficient for exact queue position, exact fills or empirical execution-cost claims |
| LOBSTER samples | Parser and reconstruction validation where files are available | Small samples are not broad empirical market evidence |
| Databento MBO or equivalent L3 data | Conditional route for order-level queue and execution modelling | Requires configured access, order IDs and appropriate permissions |
| Binance public data | Secondary public market-data ingestion or exploration | Not treated as full L3 historical LOB evidence unless audited depth-event data are confirmed |
| Controlled generated fixtures | Mechanics validation, invariants, sweep logic and accounting checks | Not empirical market evidence |

The repository stores generated fixtures, metadata, configuration, hashes and outputs. It does not redistribute paid, account-restricted, licence-restricted or large external datasets.

## Outputs

The pipeline writes public technical outputs under `reports/`, including:

- data capability and source audit tables,
- claim enforcement summaries,
- schema and feed integrity summaries,
- order book feature, liquidity, imbalance and microprice summaries,
- short-horizon label and baseline diagnostic summaries,
- execution scenario, sweep, slippage, schedule and cost attribution tables,
- impact proxy and sensitivity summaries,
- final quality, reproducibility and claim-boundary audit tables,
- figures for depth, spread, imbalance, microprice, liquidity regimes, slippage and cost attribution.

## Limitations

- Exact queue-position and exact-fill claims require L3 order-level event data with order IDs.
- Generated fixtures validate software mechanics and accounting only.
- Impact outputs are labelled as proxies and do not establish empirical market impact.
- FI-2010 is not treated as an execution reconstruction dataset.
- LOBSTER samples are used only where suitable files are available and do not support broad empirical execution-cost conclusions.
- No public output should be read as a live-trading, profitability, best-execution, broker-grade TCA or institutional execution-quality claim.

## Licence and redistribution note

The public repository is structured to avoid redistribution of restricted datasets. External data should be obtained from the original provider under the relevant licence or terms. Generated fixtures are included only for reproducible mechanics validation.

## Skills demonstrated

Python | Market microstructure | Limit order books | Execution cost modelling | Slippage analysis | Financial econometrics | Quantitative finance | Reproducible research | Research software engineering | pytest | Ruff | Parquet data pipelines
