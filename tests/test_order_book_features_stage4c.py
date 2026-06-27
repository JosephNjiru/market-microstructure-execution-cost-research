from __future__ import annotations

import pandas as pd

from microstructure_system.analytics.liquidity_regimes import summarise_liquidity_regimes
from microstructure_system.analytics.order_book_summary import summarise_order_book_features
from microstructure_system.features.imbalance import summarise_imbalance, top_level_imbalance
from microstructure_system.features.microprice import calculate_microprice, summarise_microprice


def test_order_book_feature_summary_reports_core_features(order_book_features: pd.DataFrame) -> None:
    summary = summarise_order_book_features(order_book_features)
    assert {"mid_price", "quoted_spread", "total_depth"}.issubset(set(summary["feature_name"]))


def test_imbalance_and_microprice_summaries_are_numeric(order_book_features: pd.DataFrame) -> None:
    assert top_level_imbalance(700, 300) == 0.4
    assert calculate_microprice(100.02, 100.00, 700, 300) > 100.01
    assert not summarise_imbalance(order_book_features)["mean"].isna().all()
    assert not summarise_microprice(order_book_features).empty


def test_liquidity_regime_summary_includes_invalid_books(order_book_features: pd.DataFrame) -> None:
    regimes = summarise_liquidity_regimes(order_book_features)
    assert "invalid" in set(regimes["liquidity_regime"])
