from __future__ import annotations


def adverse_slippage(side: str, execution_price: float, benchmark_price: float) -> float:
    if side == "buy":
        return max(execution_price - benchmark_price, 0.0)
    return max(benchmark_price - execution_price, 0.0)
