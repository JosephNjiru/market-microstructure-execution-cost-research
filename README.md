# Market microstructure execution cost research

Author: Joseph N. Njiru

Market microstructure execution cost research is a Python research software system for order book analytics, execution-cost mechanics, slippage diagnostics, market impact proxies and reproducible transaction cost research.

The system is built around claim-aware evidence controls. It separates public LOB benchmark evidence, parser and reconstruction samples, conditional L3 order-level data, secondary public market data and controlled generated fixtures. This prevents weaker data from supporting stronger claims than the evidence allows.

The project includes canonical schemas, data capability audits, executable claim enforcement, order book feature engineering, imbalance and microprice analytics, short-horizon movement diagnostics, marketable-order sweep mechanics, implementation shortfall, slippage benchmarks, schedule diagnostics, fill approximation, cost attribution, sensitivity analysis, final quality gates and reproducibility evidence.

## Skills demonstrated

Python | Market microstructure | Limit order books | Execution cost modelling | Slippage analysis | Financial econometrics | Quantitative finance | Reproducible research | Research software engineering | pytest | Ruff | Parquet data pipelines

## Evidence boundaries

The project does not make trading, profitability, best-execution, broker-grade transaction-cost-analysis, institutional execution-quality, live-trading, empirical execution-cost or empirical market-impact claims under the current data configuration.

FI-2010 supports LOB feature and short-horizon mid-price movement research only.
LOBSTER samples support parser and reconstruction validation only where files are available.
Databento MBO or equivalent L3 data may support exact queue-position and order-level execution claims only if access and order IDs are configured.
Binance public data is secondary ingestion evidence unless audited depth-event data are confirmed.
Generated fixtures support mechanics validation, stress checks and accounting reconciliation only.

## Repository contents

- `src/microstructure_system`: Modular source code for data audit, schemas, claim enforcement, simulation, order book analytics, execution mechanics, slippage diagnostics, impact proxies, reporting and release packaging.
- `tests`: Modular pytest suite covering source audit, claim enforcement, schemas, fixtures, features, execution, reporting, reproducibility and release exclusions.
- `config`: Stage configuration and claim policy inputs.
- `docs`: Research methodology, limitations, data capability and redistribution protocols.
- `reports`: Generated tables, figures, final report and audit evidence.

## Commands

```powershell
python -m uv run python run_project.py --stage foundation
python -m uv run python run_project.py --stage order-book
python -m uv run python run_project.py --stage execution-cost
python -m uv run python run_project.py --stage release
python -m uv run python run_project.py --stage all --config config/project_config.yaml
python -m uv run pytest
python -m uv run ruff check .
```

## Project status

The repository is structured for public review as a research software project. The current evidence scope is intentionally conservative and separates software validation, benchmark diagnostics and conditional empirical extensions.
