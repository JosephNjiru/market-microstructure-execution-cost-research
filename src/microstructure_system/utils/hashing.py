from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_record_hashes(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["record_hash"] = [
        hashlib.sha256(str(tuple(row)).encode("utf-8")).hexdigest()
        for row in output.to_numpy()
    ]
    return output
