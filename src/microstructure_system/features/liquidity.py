from __future__ import annotations


def classify_liquidity_regime(valid: bool, spread_bps: float, wide_spread_bps: float = 3.0) -> str:
    if not valid:
        return "invalid"
    if spread_bps > wide_spread_bps:
        return "wide_spread"
    return "normal"
