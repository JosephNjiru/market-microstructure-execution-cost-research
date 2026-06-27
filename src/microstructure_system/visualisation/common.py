from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def write_bar_figure(path: Path, series: pd.Series, title: str) -> None:
    """Write a compact evidence figure from a one-dimensional series."""
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 3))
    pd.Series(series).reset_index(drop=True).plot(kind="bar")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
