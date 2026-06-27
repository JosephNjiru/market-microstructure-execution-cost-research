from __future__ import annotations

import argparse
from pathlib import Path

from microstructure_system.pipeline import (
    run_execution_cost_stage,
    run_foundation_stage,
    run_order_book_stage,
    run_release_stage,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stage",
        required=True,
        choices=["foundation", "order-book", "execution-cost", "release", "all"],
    )
    parser.add_argument("--config", required=False)
    args = parser.parse_args()
    root = Path.cwd()

    if args.stage == "foundation":
        run_foundation_stage(root)
    elif args.stage == "order-book":
        run_order_book_stage(root)
    elif args.stage == "execution-cost":
        run_execution_cost_stage(root)
    elif args.stage == "release":
        run_release_stage(root)
    elif args.stage == "all":
        _ = args.config
        run_foundation_stage(root)
        run_order_book_stage(root)
        run_execution_cost_stage(root)
        run_release_stage(root)
