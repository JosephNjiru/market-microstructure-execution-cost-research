from __future__ import annotations

import pandas as pd


def summarise_execution_outputs(sweeps: pd.DataFrame) -> pd.DataFrame:
    return sweeps.groupby("execution_status").size().reset_index(name="scenario_count")
