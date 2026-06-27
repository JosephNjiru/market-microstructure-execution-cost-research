from __future__ import annotations

import pandas as pd
import pytest

from microstructure_system.execution.market_sweep import run_market_sweeps
from microstructure_system.execution.scenarios import generate_stage3_execution_scenarios
from microstructure_system.features.book_features import compute_order_book_features
from microstructure_system.features.labels import add_short_horizon_labels
from microstructure_system.simulation.lob_fixture import generate_tiny_lob_fixture


@pytest.fixture()
def tiny_book() -> pd.DataFrame:
    return generate_tiny_lob_fixture()


@pytest.fixture()
def order_book_features(tiny_book: pd.DataFrame) -> pd.DataFrame:
    return compute_order_book_features(tiny_book)


@pytest.fixture()
def short_horizon_labels(order_book_features: pd.DataFrame) -> pd.DataFrame:
    return add_short_horizon_labels(order_book_features)


@pytest.fixture()
def execution_scenarios(order_book_features: pd.DataFrame) -> pd.DataFrame:
    return generate_stage3_execution_scenarios(order_book_features)


@pytest.fixture()
def sweep_outputs(
    tiny_book: pd.DataFrame,
    execution_scenarios: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return run_market_sweeps(
        tiny_book,
        execution_scenarios[execution_scenarios["schedule_type"] == "market_sweep"],
    )
