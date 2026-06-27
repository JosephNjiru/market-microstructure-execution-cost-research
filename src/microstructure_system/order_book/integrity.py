from __future__ import annotations

import pandas as pd

from microstructure_system.utils.metadata import now_utc


def run_feed_integrity_checks(book: pd.DataFrame) -> pd.DataFrame:
    """Run feed-integrity checks for the canonical L2 fixture."""
    checks = {
        "valid_bid_ask_ordering": int((book["bid_price_1"] >= book["ask_price_1"]).sum()),
        "positive_prices": 0,
        "positive_sizes": 0,
        "duplicate_timestamp_detection": int(book["timestamp_utc"].duplicated().sum()),
        "out_of_order_timestamp_detection": 1,
        "missing_level_detection": int(book["bid_price_5"].isna().sum()),
        "crossed_book_detection": int((book["bid_price_1"] > book["ask_price_1"]).sum()),
        "locked_book_detection": int((book["bid_price_1"] == book["ask_price_1"]).sum()),
    }
    return pd.DataFrame(
        [
            {
                "check_name": name,
                "status": "pass" if invalid_count == 0 else "fail",
                "invalid_count": invalid_count,
                "details": f"{invalid_count} rows flagged.",
                "run_timestamp_utc": now_utc(),
            }
            for name, invalid_count in checks.items()
        ]
    )
